from flask import Flask, render_template, Response
import cv2
app = Flask(__name__)

video_output = None

def sendVideoOutput(frame):
    global video_output
    video_output = frame

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


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')