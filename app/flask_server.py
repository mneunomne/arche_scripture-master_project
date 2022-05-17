from flask import Flask, render_template, Response
from flask_socketio import SocketIO, send, emit
import cv2

from kiosk import run_kiosk

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

video_output = None
cropped_output = None

def sendVideoOutput(frame):
    global video_output
    video_output = frame

def sendCroppedOutput(frame):
    global cropped_output
    cropped_output = frame

def gen_frames():  # generate frame by frame from camera
    global video_output
    while True:
        # Capture frame-by-frame
        if video_output is None:
            break
        else:
            frame = video_output.copy()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

def gen_cropped():  # generate frame by frame from camera
    global cropped_output
    while True:
        # Capture frame-by-frame
        if cropped_output is None:
            break
        else:
            frame = cropped_output.copy()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cropped_feed')
def cropped_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_cropped(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('detection_data')
def sendDetectionData(data):
    emit('detection_data', data, broadcast=True)