from flask import Blueprint, request, send_from_directory, Response, render_template
import requests
from flask_socketio import emit
import time
import base64
import cv2 

from my_app import socketio
from my_app.logic.yolov8.yolo_inference import video_detection
from my_app.logic.action_recognition.videomae_inference import video_action_recognition
from my_app.logic.utils import video_chunks_save

bp_main = Blueprint('main', __name__, url_prefix="/")

chunks = [] 

@bp_main.route('/', defaults={'path': ''})
@bp_main.route('/<path:path>')
def index(path):
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client Connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client Disconnected')

@socketio.on('detection')
def inference_detection(video_data):
    video_path = 'input.mp4'
    global chunks 
    chunk = video_data['chunk']
    isLast = video_data['isLastChunk']
    chunks.append(chunk)

    if isLast:
        video_chunks_save(chunks, video_path)
        for result_img in video_detection(video_path, visualize=True):
            _, frame_buffer = cv2.imencode('.jpg', result_img)
            frame_buffer= base64.b64encode(frame_buffer)
            emit('stream_data', {'stream_frame': frame_buffer})
            time.sleep(0.05)

@socketio.on('action_recognition')
def inference_action_recognition(video_data):
    video_path = 'input.mp4'
    with open(video_path, 'wb') as f:
            f.write(video_data)

    for result_imgs in video_action_recognition(video_path, visualize=True):
        for img in result_imgs:
            _, frame_buffer = cv2.imencode('.jpg', img)
            frame_buffer= base64.b64encode(frame_buffer)
            emit('stream_data', {'stream_frame': frame_buffer})
            time.sleep(0.1)
