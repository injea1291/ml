import sys
import serial
import time
from time import sleep
import cv2.cv2 as cv
import win32con
import win32gui
import win32ui
from threading import Thread, Lock
import winsound
from models import *
from utils.datasets import *
from utils.utils import *

import random
def detect(cfg,
           names,
           weights,
           images,
           img_size=416,
           conf_thres=0.5,
           iou_thres=0.5,
           zoom=1):
    xyli = []
    device = torch_utils.select_device()
    model = Darknet(cfg, img_size)
    attempt_download(weights)
    model.load_state_dict(torch.load(weights, map_location=device)['model'])
    model.to(device).eval()

    img = letterbox(images, new_shape=img_size)[0]

    # Convert
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img, dtype=np.float32)  # uint8 to fp16/fp32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0

    classes = load_classes(names)
    img = torch.from_numpy(img).to(device)
    if img.ndimension() == 3:
        img = img.unsqueeze(0)
    pred = model(img)[0]
    pred = non_max_suppression(pred, conf_thres, iou_thres, classes=None, agnostic=False)
    for i, det in enumerate(pred):  # detections per image
        if det is not None and len(det):
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], images.shape).round()

            for *xyxy, conf, cls in det:
                label = '%s %.2f' % (classes[int(cls)], conf)
                xyxy[0:4] = list(map(lambda a: int(a) * zoom, xyxy[0:4]))
                xyli.append([label, xyxy[0], xyxy[1], xyxy[2], xyxy[3]])
            xyli.sort(key=lambda xyli: xyli[1])

    return xyli

lieimg = cv.imread('data\\samples\\384.png')
lieli = detect('cfg\\yolov3-spp-1cls.cfg', 'data\\lie.names', 'weights\\lie.pt', lieimg)

print(lieli)


