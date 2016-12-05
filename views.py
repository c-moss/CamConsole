from app import app, render_template, datetime, timedelta
from app.motioncapture import MotionCapture
from app.motiondb import get_motion_captures
from flask import request, Response
from functools import wraps
from os import getcwd, listdir
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

@app.route('/')
@app.route('/index')
@requires_auth
def index():
    displayTime = str(datetime.now()).split('.')[0]
    timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds() * 1000.0
    todayDate = datetime.now().strftime("%Y-%m-%d")
    day_str = request.args.get('day', todayDate)
    motionCaptures = getMotionCaptures(day_str)
    return render_template('index.html', motionCaptureDir=motionCaptureDir, displayTime=displayTime, timestamp=timestamp, motionCaptures=motionCaptures)
