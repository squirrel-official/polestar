import math
from ultralytics import YOLO

# Load the YOLOv8 model (replace with your desired model path)
model = YOLO('yolov8n.pt')  # You can choose other models like 'yolov8s.pt', 'yolov8m.pt', etc.


def detect_objects(image):
    # in future this needs  to be done on stream so that the all results are produced continuously
    all_results = model(image, stream=True)
    for result in all_results:
        classes = result.boxes.cls
        confidences = result.boxes.conf
        for i in range(len(classes)):
            class_type = classes[i]
            confidence = confidences[i]
            confidence = math.ceil(confidence * 100)
            if confidence > 50:
                print(class_type)
                print(confidence)
                found = True

    return found
