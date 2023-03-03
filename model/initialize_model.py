import torch
from model.yolov5 import YOLOv5

device = 'cuda' if torch.cuda.is_available() else 'cpu'
yolo = YOLOv5(device=device)
