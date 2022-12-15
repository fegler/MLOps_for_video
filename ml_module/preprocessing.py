import numpy as np
import cv2

import torch


def preprocess(im_path):
    """
        image preprocessing 
        1. image read 
        2. resize & normalize 
        3. transpose for model input 
    """
    im = cv2.imread(im_path)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    im /= 255.0
    im = np.transpose(im, (2, 0, 1))
    im_tensor = torch.tensor(im, dtype=torch.float32)
    return im_tensor.unsqueeze(0)

