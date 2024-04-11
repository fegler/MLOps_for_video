from flask import send_file, Response 

from config import Config 
from logic.yolov8.yolo_inference import yolo_inference

'''
추론 라우팅 function 
request.path 를 받아서, 해당하는 모델의 inference function 호출 
'''
def inference(task, video_file):
    if task == '/detection':
        return yolo_inference(video_file)
    elif task == '/action_recognition':
        pass 