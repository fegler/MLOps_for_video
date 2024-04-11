from werkzeug.utils import secure_filename
from flask import request, send_file, Response

import os
import cv2 

from config import Config

def upload_video(video_file):
    video_file = request.files['video']

    if video_file.filename == '':
        return 'No selected file'

    if video_file:
        filename = secure_filename(video_file.filename)
        video_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        video_file.save(video_path)
        return 'Video uploaded successfully'

def frame_reader(video_path):
    video = cv2.VideoCapture(video_path)
    frames = [] 
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
        frames.append(frame)
    return frames