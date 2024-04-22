import math
from ultralytics import YOLO

# Load the YOLOv8 model (replace with your desired model path)

model = YOLO('yolov8s.pt')  # You can choose other models like 'yolov8n.pt','yolov8s.pt', 'yolov8m.pt', etc.


def detect_objects(image, timestamp, dir_path):
    # in future this needs  to be done on stream so that the all results are produced continuously
    all_results = model(image, stream=True)
    for result in all_results:
        classes = result.boxes.cls
        confidences = result.boxes.conf
        for i in range(len(classes)):
            class_type = classes[i]
            confidence = confidences[i]
            confidence = math.ceil(confidence * 100)
            if class_type == 0 and confidence > 70:
                print("Human found,saving picture")
                complete_file_name = dir_path + str(timestamp) + '.jpg'
                result.save(filename=complete_file_name)
                return True

    return False
