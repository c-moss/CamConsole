from app import app, render_template, datetime
from app.motioncapture import MotionCapture
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

def getMotionCaptures():
    motionCapturePath = "app" + motionCaptureDir
    motionCaptures = []
    fileList = [f for f in listdir(motionCapturePath) if (isfile(join(motionCapturePath, f)))]
    fileList.sort()
    for filename in fileList:
        if filename.endswith(".mp4"):
            videoFile = filename
            imageFile = filename.rsplit(".",1)[0] + ".jpg"
            motionCapture = MotionCapture(videoFile=videoFile)
            if (isfile(join(motionCapturePath, imageFile))):
                motionCapture.imageFile = imageFile
            motionCaptures.append(motionCapture)
        
    return motionCaptures

@app.route('/')
@app.route('/index')
@requires_auth
def index():
    displayTime = str(datetime.now()).split('.')[0]
    timestamp = (datetime.now() - datetime.fromtimestamp(0)).total_seconds() * 1000.0
    motionCaptures = getMotionCaptures()
    return render_template('index.html', motionCaptureDir=motionCaptureDir, displayTime=displayTime, timestamp=timestamp, motionCaptures=motionCaptures)
