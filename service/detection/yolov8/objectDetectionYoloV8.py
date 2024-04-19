import cv2
from ultralytics import YOLO

# Load the YOLOv8 model (replace with your desired model path)
model = YOLO('yolov8n.pt')  # You can choose other models like 'yolov8s.pt', 'yolov8m.pt', etc.


def detect_objects(image):
    results = model(image, stream=True)
    print('anil1')
    print(results)

    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        print('Anil-boxes')
        print(boxes)
        print('Anil-masks')
        print(masks)
        print('Anil-keypoints')
        print(keypoints)
        print('Anil-probs')
        print(probs)
