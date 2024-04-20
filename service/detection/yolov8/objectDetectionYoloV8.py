import cv2
import math
from ultralytics import YOLO

# Load the YOLOv8 model (replace with your desired model path)
model = YOLO('yolov8n.pt')  # You can choose other models like 'yolov8s.pt', 'yolov8m.pt', etc.


def detect_objects(image):
    results = model(image, stream=True)
    print('anil1')
    print(results)
    print(type(results))

    found = False

    for result in results:
        boxes = result.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values

            # put box in cam
            # cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # confidence
            confidence = math.ceil((box.conf[0] * 100)) / 100
            print("Confidence --->", confidence)
            found = True
            # class name
            cls = int(box.cls[0])
            print("Class name -->", cls)

    return found

    # for result in results:
    #     boxes = result.boxes  # Boxes object for bounding box outputs
    #     masks = result.masks  # Masks object for segmentation masks outputs
    #     keypoints = result.keypoints  # Keypoints object for pose outputs
    #     probs = result.probs  # Probs object for classification outputs
    # print('Anil-boxes')
    # print(boxes)
    # print('Anil-masks')
    # print(masks)
    # print('Anil-keypoints')
    # print(keypoints)
    # print('Anil-probs')
    # print(probs)
