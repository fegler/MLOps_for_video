import os 

BASE_DIR = os.path.dirname(__file__)
INFER_SERVER_IP = '0.0.0.0'
INFER_SERVER_PORT = '0000'
INFERENCE_URI = f'http://{INFER_SERVER_IP}:{INFER_SERVER_PORT}'
SECRET_KEY = 'secret'