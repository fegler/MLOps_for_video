from flask import Blueprint, request, send_file, Response, render_template
import requests
from flask_socketio import emit
import time
import base64

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

@socketio.on('detection')
def inference_detection(video_data):
    print('detection call')
    import cv2 
    from my_app.logic.yolov8 import yolo_inference
    video_path = 'input.mp4'
    with open(video_path, 'wb') as f:
        f.write(video_data)
    
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        result_img, _ = yolo_inference.yolo_inference(frame, visualize=True)
        if not ret:
            break 
        _, frame_buffer = cv2.imencode('.jpg', result_img)
        frame_buffer= base64.b64encode(frame_buffer)
        emit('stream_data', {'stream_frame': frame_buffer})
        time.sleep(0.1)
