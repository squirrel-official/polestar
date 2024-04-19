import cv2
from ultralytics import YOLO

# Load the YOLOv8 model (replace with your desired model path)
model = YOLO('yolov8n.pt')  # You can choose other models like 'yolov8s.pt', 'yolov8m.pt', etc.


def detect_objects(image):
    # prediction = model.predict(image)
    # print('prediction')
    # print(prediction)
    # print('type(prediction)')
    # print(type(prediction))
    results = model(image, stream=True)
    print('anil1')
    print(results)
    # print('anil2')
    # print(results[0])
    # print('anil3')
    # print(results[0].pandas())
    # print('anil4')

    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        print('boxes')
        print(boxes)
        print('masks')
        print(masks)
        print('keypoints')
        print(keypoints)
        print('probs')
        print(probs)

    objects_df = results[0].pandas().xyxy[0]
    if objects_df.shape[0] > 0:  # Check if any objects were detected
        print('Objects detected:')
        print(objects_df)
        for x_min, y_min, x_max, y_max, conf, name in objects_df.values:
            cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
            cv2.putText(image, f"{name} ({conf:.2f})", (int(x_min), int(y_min) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 255, 0), 2)
        return True
    else:
        print('No objects detected.')
        return False

