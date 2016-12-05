import sqlite3
from app import app
from app.motioncapture import MotionCapture
from flask import g

DATABASE = '/home/web/CamConsole/db/camconsole.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return rv if rv else None

def map_db_object_motion_capture(rec):
    return MotionCapture(cameraId=rec['camera'], fileName=rec['filename'], frame=rec['frame'], fileType=rec['file_type'], timestamp=rec['time_stamp'], eventTimestamp=rec['event_time_stamp'])

def get_motion_captures(from_day, to_day):
    captures = query_db("select * from security where file_type = 8 and time_stamp > '{0}' and time_stamp < '{1}' and not filename like '%.avi'".format(from_day, to_day))
    if captures is not None:
        return list(map(map_db_object_motion_capture, captures))
    else:
        return []
