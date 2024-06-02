import cv2
import numpy as np
import torch
import os
import pyautogui
from ultralytics import YOLO
from util import *

# Initialize the camera (webcam)
capture = cv2.VideoCapture(1)

if not capture.isOpened():
    print("Error: Could not open camera.")
    exit()

# Set dimensions for capturing screen
screen_width = 1920
screen_height = 1080
width = 640  # Input size the model was trained on
height = 640  # Input size the model was trained on
roi_x = screen_width // 2 - width // 2
roi_y = screen_height // 2 - height // 2

# Set camera dimensions
capture.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

# Output window
cv2.namedWindow('Capture', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Capture', width, height)

# Load the YOLO model
model = YOLO('weights/second_gen_best(maybe not).pt')

while True:
    # Capture screen
    #frame = captureFrame(capture, roi_x, roi_y, width, height)
    #if len(frame) == 0:
        #break
    screen = pyautogui.screenshot(region=(roi_x, roi_y, width, height))
    frame = np.array(screen)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Resize frame to match input size of YOLO model
    frame = cv2.resize(frame, (640, 640))

    #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2RGB)

    # Perform object detection
    results = model(frame, verbose=False, conf=0.4)
    boxes = results[0].boxes  # Get the boxes object from the first result

    for box in boxes:
        x_min, y_min, x_max, y_max = box.xyxy[0]
        x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 3)

    # Display the frame with detected objects
    cv2.imshow('Capture', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture device and close all OpenCV windows
capture.release()
cv2.destroyAllWindows()
