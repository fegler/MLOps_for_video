import torch 
from torch.utils.data import Dataset 
from decord import VideoReader, cpu 
import random 

class VideoDataset(Dataset):
    def __init__(self, video_list, labels, processor, num_frames=16, train=True):
        self.video_list = video_list
        self.labels = labels
        self.processor = processor 
        self.num_frames = num_frames 
        self.train = train 

    def __len__(self):
        return len(self.video_list)
    
    def __getitem__(self, idx):
        path = self.video_list[idx]
        label = self.labels[idx]

        vr = VideoReader(path, ctx=cpu(0))
        total_frames = len(vr)

        if total_frames < self.num_frames:
            raise ValueError(f"Video too short: {path}")
        
        if self.train:
            start_idx = random.randint(0, total_frames - self.num_frames)
        else:
            start_idx = (total_frames - self.num_frames) // 2 ## center sampling 
        
        frame_indices = list(range(start_idx, start_idx + self.num_frames))
        frames = vr.get_batch(frame_indices).asnumpy() ## T, H, W, C 

        ## hugging face model input data processor 
        ### expects PIL.Image or numpy array 
        processed = self.processor(
            list(frames),
            return_tensors="pt"
        )

        pixel_values = processed["pixel_values"]

        return {
            "pixel_values": pixel_values.squeeze(), 
            "labels": torch.tensor(label, dtype=torch.long)
        }