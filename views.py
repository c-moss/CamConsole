from app import app, render_template, datetime, timedelta
from app.motioncapture import MotionCapture
from app.motiondb import get_motion_captures
from flask import request, Response, redirect
from functools import wraps
from os import getcwd, listdir, statvfs
from os.path import isfile, join

motionCaptureDir = "/static/motion"

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'camera' and password == 'SekritSpyCam'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def getMotionCaptures(day_str):
    from_day = datetime.strptime(day_str, "%Y-%m-%d")
    to_day = from_day + timedelta(days=1)
    return get_motion_captures(from_day.strftime("%Y-%m-%d"), to_day.strftime("%Y-%m-%d"))

def usage_percent(used, total, _round=None):
    """Calculate percentage usage of 'used' against 'total'."""
    try:
        ret = (used / total) * 100
    except ZeroDivisionError:
        ret = 0.0 if isinstance(used, float) or isinstance(total, float) else 0
    if _round is not None:
        return round(ret, _round)
    else:
        return ret

def format_disk_space(size):
   if size < 1024:
       return "{0}B".format(size)
   elif size < (1024*1024):
       return "{0}KB".format(round(size/1024,1))
   elif size < (1024*1024*1024):
       return "{0}MB".format(round(size/(1024*1024),1))
   elif size < (1024*1024*1024*1024):
       return "{0}GB".format(round(size/(1024*1024*1024),1))
   else:
       return "{0}TB".format(round(size/(1024*1024*1024*1024),1))

def disk_usage(path):
    """Return disk usage associated with path."""
    try:
        st = statvfs(path)
    except UnicodeEncodeError:
        if not PY3 and isinstance(path, unicode):
            # this is a bug with os.statvfs() and unicode on
            # Python 2, see:
            # - https://github.com/giampaolo/psutil/issues/416
            # - http://bugs.python.org/issue18695
            try:
                path = path.encode(sys.getfilesystemencoding())
            except UnicodeEncodeError:
                pass
            st = statvfs(path)
        else:
            raise
    free = format_disk_space(st.f_bavail * st.f_frsize)
    total = (st.f_blocks * st.f_frsize)
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    percent = usage_percent(used, total, _round=1)
    # NB: the percentage is -5% than what shown by df due to
    # reserved blocks that we are currently not considering:
    # http://goo.gl/sWGbH
    return {'total': total, 'used': used, 'free': free, 'percent': percent}

@app.route('/')
@app.route('/index')
@requires_auth
def index():
    displayTime = str(datetime.now()).split('.')[0]
    timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds() * 1000.0
    todayDate = datetime.now().strftime("%Y-%m-%d")
    day_str = request.args.get('day')
    if day_str:
        motionCaptures = getMotionCaptures(day_str)
        return render_template('index.html', motionCaptureDir=motionCaptureDir, displayTime=displayTime, timestamp=timestamp, motionCaptures=motionCaptures)
    else:
        return redirect("/?day={0}".format(todayDate), code=302)

@app.route('/status')
@requires_auth
def status():
    return render_template('status.html', file_stats=disk_usage("/"))
