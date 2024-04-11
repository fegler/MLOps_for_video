from flask import Blueprint, request, send_file, Response, render_template
import requests
from flask_socketio import emit
import time
import base64

from my_app.logic.yolov8 import yolo_inference
from config import Config
from my_app import socketio

bp_main = Blueprint('main', __name__, url_prefix="/")

@bp_main.route('/')
def index():
    # return 'Hello Server!'
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client Connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client Disconnected')

@socketio.on('process_video')
def process_video(video_data):
    print('Processing Video')
    import cv2 
    video_path = 'input.mp4'
    with open(video_path, 'wb') as f:
        f.write(video_data)
    
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break 
        _, frame_buffer = cv2.imencode('.jpg', frame)
        frame_buffer= base64.b64encode(frame_buffer)
        emit('stream_data', {'stream_frame': frame_buffer.tobytes()})
        time.sleep(0.1)

    cap.release()

# Route to handle video upload
@bp_main.route('/detection', methods=['POST'])
def infer_detection():
    if 'video' not in request.files:
        return 'No file part'
    video_file = request.files['video']
    return Response(
        yolo_inference.yolo_inference_video(video_file),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )