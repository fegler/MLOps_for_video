import cv2 
import numpy as np 
from collections import deque
import sys, os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ultralytics import YOLO 

import config

yolo_model = YOLO(f'{config.INFER_SERVER_IP}:{config.INFER_SERVER_PORT}/yolov8l', task='detect')

def yolo_inference(input_image, visualize=False, box_margin=0.0):
    pred = yolo_model.predict(input_image, classes=[0])
    box = pred[0].boxes.xyxy.cpu().numpy()

    input_image, box = postprocess(
        input_image, box, 
        visualize=visualize, box_margin=box_margin
    )

    return input_image, box 

def postprocess(input_image, boxes, visualize=False, box_margin=0.0):
    h, w, _ = input_image.shape
    scaled_boxes = []
    for box in boxes: 
        box_h, box_w = box[3]-box[1], box[2]-box[0]
        scale_h, scale_w = box_margin*box_h, box_margin*box_w
        box[0] = max(0, box[0]-scale_w)
        box[1] = max(0, box[1]-scale_h)
        box[2] = min(w, box[2]+scale_w)
        box[3] = min(h, box[3]+scale_h)
        box = [int(b) for b in box]
        scaled_boxes.append(box)

        if visualize:
            input_image = cv2.rectangle(
                input_image, 
                (int(box[0]), int(box[1])), 
                (int(box[2]), int(box[3])), 
                (0, 0, 255), 2)
    return input_image, scaled_boxes

if __name__ == '__main__':
    video = cv2.VideoCapture(r'C:\Users\DJ\tmax\ai_demo\uploads\C00_018_0012.mp4_clip_2.mp4')
    yolo_model = YOLO(f'{config.INFER_SERVER_IP}:{config.INFER_SERVER_PORT}/yolov8l', task='detect')
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break

        # inference 
        return_image, box = yolo_inference(frame, visualize=True)
        print(box)
        print(return_image.shape)
        cv2.imwrite(r'C:\Users\DJ\tmax\ai_demo\uploads\output.jpg', return_image)
        

        break