import cv2
import numpy as np
import torch
import os
from ultralytics import YOLO
from util import *
from PIL import Image
capture = cv2.VideoCapture(0)  # should be 0 on Raspberry Pi

if not capture.isOpened():
    print("Error: Could not open camera.")
    exit()

# get user path
user_home = os.path.expanduser("~")

screen_width = 1920
screen_height = 1080
width = 400
height = 400
roi_x = screen_width // 2 - width // 2
roi_y = screen_height // 2 - height // 2

# set width and height
capture.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

# output window
cv2.namedWindow('Capture', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Capture', 400, 400)

# load model
model = YOLO('weights/first_gen_best.pt')


frame = cv2.imread(
    "../train_yolo_+_dataset/third_dataset/images/train/Breachenemy00701_jpg.rf.b41b36d8b8d9b8a9735235dda9a36cdb.jpg")
results = model.predict(source=frame, save=True, save_txt=True)
#boxes = results[0].boxes  # Get the boxes object from the first result

#for box in boxes:
    #x_min, y_min, x_max, y_max = box.xyxy[0]
    #x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)
    #cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 3)

cv2.imshow('Capture', frame)


# Release the capture device and close all OpenCV windows
capture.release()
cv2.destroyAllWindows()