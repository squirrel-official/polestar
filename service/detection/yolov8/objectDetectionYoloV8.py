import cv2
from ultralytics import YOLO

# Load the YOLOv8 model (replace with your desired model path)
model = YOLO('yolov8n.pt')  # You can choose other models like 'yolov8s.pt', 'yolov8m.pt', etc.


def detect_objects(image):
    results = model(image, stream=True)
    print('anil1')
    print(results)
    print(type(results))

    high_probability_objects = []
    for class_label, confidence, bbox in results:
        if confidence > 0.5:  # Adjust threshold as needed
            high_probability_objects.append((class_label, confidence, bbox))

    if high_probability_objects:
        print("High probability objects detected:")
        for class_label, confidence, bbox in high_probability_objects:
            print(f"Class: {class_label}, Confidence: {confidence}, Bounding Box: {bbox}")
    else:
        print("No high probability objects detected.")

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
