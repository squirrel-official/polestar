import math
from ultralytics import YOLO
import cv2

# Load the YOLOv8 model (replace with your desired model path)
model = YOLO('yolov8n.pt')  # You can choose other models like 'yolov8s.pt', 'yolov8m.pt', etc.


def detect_objects(image):
    # in future this needs  to be done on stream so that the all results are produced continuously
    all_results = model(image, stream=True)
    found = False
    for result in all_results:
        print(result.boxes.xyxy)
        boxes = result.boxes.xyxy
        classes = result.boxes.cls
        confidences = result.boxes.conf
        for i in range(len(classes)):
            class_type = classes[i]
            confidence = confidences[i]
            confidence = math.ceil(confidence * 100)
            x_min, y_min, x_max, y_max = boxes[i]

            if confidence > 50:
                print(class_type)
                print(confidence)
                print(type(x_min))
                print(type(x_max))
                image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                cv2.rectangle(image_bgr, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                found = True

    return found
