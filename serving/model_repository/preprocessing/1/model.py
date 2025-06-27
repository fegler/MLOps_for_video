import torch
import numpy as np
from transformers import VideoMAEImageProcessor
from decord import VideoReader, cpu
from PIL import Image
import io

import triton_python_backend_utils as pb_utils

class TritonPythonModel:
    def initialize(self, args):
        self.processor = VideoMAEImageProcessor.from_pretrained("MCG-NJU/videomae-base")
        self.num_frames = 16 

    def execute(self, requests):
        responses = [] 
        for request in requests:
            raw_video = pb_utils.get_input_tensor_by_name(request, "raw_video")
            video_bytes = raw_video.as_numpy().tobytes() 

            try:
                vr = VideoReader(io.BtyesIO(video_bytes), ctx=cpu(0))
                total_frames = len(vr)

                if total_frames < self.num_frames:
                    raise ValueError(f"Video too short: only {total_frames} frame")
            
                start_idx = (total_frames - self.num_frames) // 2 
                frame_indices = list(range(start_idx, start_idx + self.num_frames))
                frames = vr.get_batch(frame_indices).asnumpy() ## T, H, W, C 

                processed = self.processor(
                    list(frames), return_tensors="np"
                )

                pixel_values = processed["pixel_values"] # 1, T, C, H, W 
                out_tensor = pb_utils.Tensor.from_numpy("pixel_values", pixel_values)
                responses.append(
                    pb_utils.InferenceResponse(output_tensors=[out_tensor])
                )
            except Exception as e:
                error_message = f"Preprocessing failed: {str(e)}"
                responses.append(pb_utils.InferenceResponse(
                    output_tensors=[],
                    error=pb_utils.TritonError(error_message)
                ))

        return responses