import math
from ultralytics import YOLO
import time
# Load the YOLOv8 model (replace with your desired model path)

model = YOLO('yolov8n.pt')  # You can choose other models like 'yolov8s.pt', 'yolov8m.pt', etc.


def detect_objects(image, timestamp, dir_path):
    start_date_time = time.time()
    # in future this needs  to be done on stream so that the all results are produced continuously
    all_results = model(image, stream=True)
    found = False
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
                print("Object detected, now saving it")
                complete_file_name = dir_path + str(timestamp) + '.jpg'
                result.save(filename= complete_file_name)
                found = True

    print("total time {0} seconds".format( (time.time() - start_date_time)))
    return found
