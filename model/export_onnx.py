import os 
import torch 
from transformers import VideoMAEForVideoClassification, VideoMAEImageProcessor

EXP_PATH = './exp/test'
MODEL_DIR = f'{EXP_PATH}/checkpoint-best'
MODEL_NAME = "MCG-NJU/videomae-base"
SAVE_PATH = f"{EXP_PATH}/model.onnx"

## 1. Load model 
model = VideoMAEForVideoClassification.from_pretrained(
    MODEL_DIR, 
    ignore_mismatched_sizes=True,
).eval() 

## 2. Dummy Input (B, T, C, H, W)
batch_size, num_frames, channels, height, width = 1, 16, 3, 224, 224 
dummy_input = torch.randn(batch_size, num_frames, channels, height, width)

## 3. ONNX Export 
torch.onnx.export(
    model, 
    dummy_input, 
    SAVE_PATH, 
    input_names=["pixel_values"],
    output_names=["logits"],
    dynamic_axes={
        "pixel_values": {0: "batch_size", 1: "num_frames"},
        "logits": {0: "batch_size"},
    },
    opset_version=17,
)

print(f"Exported ONNX model to: {SAVE_PATH}")