import cv2
import math
from ultralytics import YOLO

# Load the YOLOv8 model (replace with your desired model path)
model = YOLO('yolov8n.pt')  # You can choose other models like 'yolov8s.pt', 'yolov8m.pt', etc.


def detect_objects(image):
    # print(model.names)
    all_results = model(image, stream=True)
    for result in all_results:
        print('ANil23')
        print(result)
        print('ANil23')

    results = [obj for obj in all_results if obj[0] == "person"]

    print(type(results))
    print(results)

    found = False
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # confidence
            confidence = math.ceil((box.conf[0] * 100)) / 100
            print("Confidence --->", confidence)
            found = True
            # class name
            cls = int(box.cls[0])
            print("Class name -->", cls)

    return found
