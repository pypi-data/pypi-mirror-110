from yolo import YOLO

import cv2
import numpy as np
from PIL import Image
import os
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

from keras.models import load_model
import requests
import os
import gdown
import cv2
from mtcnn.mtcnn import MTCNN
import dlib
import sys
sys.path.append('../')
from utils import model_utils


yolo3 = None
yolo4 = None

def yolo3_detect(frame, class_names=None):
    global yolo3
    frame = Image.fromarray(frame)
    if yolo3 is None:
        model_utils.get_yolov3()
        yolo3 = YOLO()
    out_boxes, out_scores, out_classes = yolo3.detect_image(frame)
    boxes = []
    for box in out_boxes:
        top, left, bottom, right = box
        top = max(0, np.floor(top + 0.5).astype('int32'))
        left = max(0, np.floor(left + 0.5).astype('int32'))
        bottom = min(frame.size[1], np.floor(bottom + 0.5).astype('int32'))
        right = min(frame.size[0], np.floor(right + 0.5).astype('int32'))
        boxes.append([left,top,right,bottom])

    classes = [yolo3.class_names[i] for i in out_classes]
    return boxes, out_scores, classes

def test():
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    while ret:
        ret, frame = video_capture.read()  # frame shape 640*480*3
        boxes, scores, classes = yolo3_detect(frame)
        for i,bbox in enumerate(boxes):
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),(255,255,255), 2)
            cv2.putText(frame, str(classes[i]),(int(bbox[0]), int(bbox[1])),0, 5e-3 * 100, (0,255,0),2)
        cv2.imshow('Show', frame)
        k=cv2.waitKey(1)
        if k == ord('q'):
            break

if __name__ == '__main__':
    test()
