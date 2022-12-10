from flask import Flask, render_template, Response
import cv2
from server_camera import camera
 
class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,1920)
        self.cap.set(4,1080)
        
    
    def __del__(self):
        self.cap.release()
    
    def get_frame(self):
        ret,image = self.cap.read()
        jpeg = cv2.imencode('.jpg', image)
        return jpeg[1].tobytes()

app = Flask(__name__)
 
@app.route('/') 
def index():
    return render_template('index.html')
 
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
 
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    