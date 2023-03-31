from flask import Flask, Response, render_template
import cv2
from services import video_gener

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    
    gener = video_gener.VideoGenerator()
    return Response(gener.get_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()
