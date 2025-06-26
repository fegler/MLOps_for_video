import os 
import sys 
import numpy as np 
from glob import glob
import random
import warnings
warnings.filterwarnings("ignore", message="Creating a tensor from a list of numpy.ndarrays*")

import torch 
from transformers \
    import VideoMAEForVideoClassification, VideoMAEImageProcessor, \
        TrainingArguments, Trainer
print(TrainingArguments)
print(TrainingArguments.__init__.__code__.co_filename)
import evaluate 
from sklearn.model_selection import train_test_split 

from dataset import VideoDataset

DATA_DIR = "../data"
TEST_RATIO = 0.2
EXP_PATH = './exp/test'
NUM_EPOCH = 10 
BATCH_SIZE = 4 
OPTIM = 'adamw'
LR = 5e-5 

## 1. Data Setting 
class_names = os.listdir(DATA_DIR)
num_class = len(class_names)
videos, labels = [], [] 
for idx, c_name in enumerate(class_names):
    v = glob(os.path.join(DATA_DIR, c_name, '*.mp4'))
    videos += v 
    labels += [idx for _ in range(len(v))]

train_videos, val_videos, train_labels, val_labels = train_test_split(
    videos, labels, 
    test_size=TEST_RATIO,
    stratify=labels,
    random_state=42
)

## 2. Processor + Dataset 
processor = VideoMAEImageProcessor.from_pretrained("MCG-NJU/videomae-base")
train_dataset = VideoDataset(train_videos, train_labels, processor, train=True)
val_dataset = VideoDataset(val_videos, val_labels, processor, train=False)

## 3. Model Setting 
model = VideoMAEForVideoClassification.from_pretrained(
    "MCG-NJU/videomae-base", 
    num_labels=num_class
)

## 4. Metric 
accuracy = evaluate.load("accuracy")
def compute_metrics(p):
    preds = np.argmax(p.predictions, axis=1)
    return accuracy.compute(predictions=preds, references=p.label_ids)

## 5. Train Setting
trainer_args = TrainingArguments(
    output_dir=EXP_PATH,
    remove_unused_columns=False,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    save_total_limit=1,
    dataloader_num_workers=4,
    learning_rate=LR,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    warmup_ratio=0.1,
    logging_steps=10,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    max_steps=(len(train_dataset) // BATCH_SIZE) * NUM_EPOCH,

)

## 6. Trainer
trainer = Trainer(
    model,
    trainer_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics
)

# 7. Train & Evaluate
trainer.train()
trainer.evaluate()