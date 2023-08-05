import sys
sys.path.append('../')
from ..utils import model_utils
from ..face.detection import ssd_detect

from .deep_sort import preprocessing
from .deep_sort import nn_matching
from .deep_sort.detection import Detection
from .deep_sort.tracker import Tracker
from .tools import generate_detections as gdet
import cv2
import numpy as np
import os
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'


max_cosine_distance = 0.2 # 0.3
nn_budget = 100 # none
nms_max_overlap = 1.0

# # Deep SORT
model_dir = os.path.join(os.path.expanduser('~'), '.duyai/model')

model_utils.get_deepsort()
encoder = gdet.create_box_encoder(model_dir + '/mars_deepsort.pb',batch_size=1)
metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
tracker = Tracker(metric)

def tracking(frame, boxes, confidence=None):
    if len(boxes)>0:
        boxes = [[b[0], b[1], abs(b[0]-b[2]), abs(b[1]-b[3])] for b in boxes] # convert [x1,y1,x2,y2] to [x,y,w,h]
        features = encoder(frame,boxes)
        if confidence == None:
            confidence = [0.8]*len(boxes)
        detections = [Detection(bbox, confidence, feature) for bbox, confidence, feature in zip(boxes, confidence, features)]

        boxes = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        indices = preprocessing.non_max_suppression(boxes, nms_max_overlap, scores)
        detections = [detections[i] for i in indices]

        # Call the tracker
        tracker.predict()
        tracker.update(detections)

        new_boxes = []
        ids = []
        for track in tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue 
            bbox = track.to_tlbr()
            new_boxes.append(np.array(bbox).astype("int"))
            ids.append(track.track_id)
        
        return np.array(new_boxes), ids
    else:
        return [], []

def test():
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    while ret:
        ret, frame = video_capture.read()  # frame shape 640*480*3
        boxes = ssd_detect(frame)
        boxes, ids = tracking(frame, boxes)
        for i,bbox in enumerate(boxes):
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),(255,255,255), 2)
            cv2.putText(frame, str(ids[i]),(int(bbox[0]), int(bbox[1])),0, 5e-3 * 100, (0,255,0),2)
        cv2.imshow('Show', frame)
        k=cv2.waitKey(1)
        if k == ord('q'):
            break
        
        
if __name__ == '__main__':
    test()

