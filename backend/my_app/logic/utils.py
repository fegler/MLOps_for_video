import cv2 
import numpy as np 

def normalize_image(image, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]):
    ## image => (0 ~ 1 range values)
    ## image size => C, H, W
    mean = np.array(mean)[:, np.newaxis, np.newaxis]
    std = np.array(std)[:, np.newaxis, np.newaxis]
    return (image - mean) / std

def softmax_np(x):
    return np.exp(x) / np.sum(np.exp(x), axis=-1, keepdims=True)