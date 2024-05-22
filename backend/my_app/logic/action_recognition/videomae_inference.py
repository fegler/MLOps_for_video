import cv2 
import numpy as np 
import sys, os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

import config 
from my_app.logic.yolov8.yolo_inference import yolo_inference
from my_app.logic.utils import normalize_image, softmax_np

import tritonclient.http as httpclient

model_url = f'{config.INFERENCE_URI}'
model_name = 'videomae'
action_class = ['Normal', 'Fight']

def request_to_trt(input_data):
    client = httpclient.InferenceServerClient(model_url)
    input_req = [httpclient.InferInput('input_clip', input_data.shape, 'FP32')]
    input_req[0].set_data_from_numpy(input_data)
    outputs = [httpclient.InferRequestedOutput('output_prob')]

    response = client.infer(model_name,
                            input_req,
                            outputs=outputs)
    response = response.as_numpy('output_prob')
    return response

def video_action_recognition(video_path, visualize=True, clip_duration=2):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(5)
    frames = []
    n_frame = 0
    frame_period = int((fps*clip_duration) // 16)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if n_frame % frame_period == 0:
            frames.append(frame)
        n_frame += 1
        if len(frames) == 16:
            visualize_frames = frames.copy()
            print(len(visualize_frames))
            clip_inputs, boxes = preprocess(frames)
            frames = []
            for idx, box in enumerate(boxes):
                ## each person action recognition 
                response = request_to_trt(clip_inputs[idx])
                visualize_frames = postprocess(visualize_frames, box, response)
            yield visualize_frames

def preprocess(frames):
    _, det_box = yolo_inference(
        frames[len(frames)//2], 
        visualize=False, box_margin=0.1
    )
    frames = np.stack(frames, axis=0) ## N, H, W, C
    clip_inputs = [] 
    if len(det_box) == 0:
        return [], []
    for box in det_box:
        clip_input = frames[:, box[1]:box[3], box[0]:box[2], :]
        clip_input = clip_input.astype(np.float32) / 255.0 # to (0~1) range
        clip_input = [
            normalize_image(
                (cv2.resize(im, (224, 224))).transpose(2, 0, 1)
            ) for im in clip_input
        ]
        clip_input = np.stack(clip_input, axis=0).astype(np.float32)
        clip_input = np.expand_dims(clip_input, 0) ## 16 3 224 224
        clip_inputs.append(clip_input)
    return clip_inputs, det_box

def postprocess(frames, box, response):
    prob = softmax_np(response) ## 1x2
    action = action_class[np.argmax(prob)]
    for frame in frames:
        cv2.rectangle(frame,
                      (box[0], box[1]),
                    (box[2], box[3]),
                    (0, 0, 255), 2
        )
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (box[0], box[1]-10)
        font_scale = 0.5 
        font_color = (0, 0, 255)
        line_type = 2 
        cv2.putText(frame, action, org, font, font_scale, font_color, line_type)
    return frames

if __name__ == '__main__':
    video_path = r'C:\Users\DJ\tmax\ai_demo\uploads\C00_018_0012.mp4_clip_2.mp4'
    for result in video_action_recognition(video_path, visualize=True):
        pass