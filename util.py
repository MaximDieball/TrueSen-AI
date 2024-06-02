import cv2

def captureFrame(capture, roi_x, roi_y, width, height):
    ret, frame = capture.read()

    if not ret:
        return []

    return frame[roi_y:roi_y + height, roi_x:roi_x + width]