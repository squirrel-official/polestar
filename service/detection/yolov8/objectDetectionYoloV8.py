import cv2
from ultralytics import YOLO

# Load the YOLOv8 model (replace with your desired model path)
model = YOLO('yolov8n.pt')  # You can choose other models like 'yolov8s.pt', 'yolov8m.pt', etc.


def detect_objects(image):
    results = model(image)
    if results.pandas().xyxy[0].shape[0] > 0:  # Check if any objects were detected
        for x_min, y_min, x_max, y_max, conf, name in results.pandas().xyxy[0].values:
            cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
            cv2.putText(image, f"{name} ({conf:.2f})", (int(x_min), int(y_min) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 255, 0), 2)
        return True
    else:
        return False
