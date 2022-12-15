from main_module import ResnetModule
from preprocessing import preprocess

"""
    ml module api 
    1. load module 
    2. inference 
"""


def inference(im_path):

    ## load module
    model = ResnetModule()

    ## input setting
    input_im = preprocess(im_path)

    ## inference
    result = model(input_im)
    return result

