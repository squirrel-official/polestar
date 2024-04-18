import os
import cv2
import numpy as np
from importlib.util import find_spec
from tensorflow.lite.python.interpreter import Interpreter

def tensor_coco_ssd_mobilenet(image):
    model_name = '/usr/local/polestar/model/coco-ssd-mobilenet'
    graph_name = 'detect.tflite'
    labelmap_name = 'labelmap.txt'
    min_conf_threshold = 0.65
    use_tpu = False

    if find_spec('tflite_runtime'):
        from tflite_runtime.interpreter import load_delegate
    else:
        from tensorflow.lite.python.interpreter import load_delegate

    if use_tpu and graph_name == 'detect.tflite':
        graph_name = 'edgetpu.tflite'

    cwd_path = os.getcwd()
    path_to_ckpt = os.path.join(cwd_path, model_name, graph_name)
    path_to_labels = os.path.join(cwd_path, model_name, labelmap_name)

    with open(path_to_labels, 'r') as f:
        labels = [line.strip() for line in f.readlines()]
    if labels[0] == '???':
        del labels[0]

    if use_tpu:
        interpreter = Interpreter(model_path=path_to_ckpt, experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    else:
        interpreter = Interpreter(model_path=path_to_ckpt)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    height, width = input_details[0]['shape'][1:3]
    floating_model = input_details[0]['dtype'] == np.float32

    outname = output_details[0]['name']
    if 'StatefulPartitionedCall' in outname:
        boxes_idx, classes_idx, scores_idx = 1, 3, 0
    else:
        boxes_idx, classes_idx, scores_idx = 0, 1, 2

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imH, imW, _ = image.shape
    image_resized = cv2.resize(image, (width, height))
    input_data = np.expand_dims(image_resized, axis=0)

    if floating_model:
        input_data = (np.float32(input_data) - 127.5) / 127.5

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0]
    classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0]
    scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0]

    object_found = False
    for i in range(len(scores)):
        if min_conf_threshold < scores[i] <= 1.0:
            ymin = int(max(1, (boxes[i][0] * imH)))
            xmin = int(max(1, (boxes[i][1] * imW)))
            ymax = int(min(imH, (boxes[i][2] * imH)))
            xmax = int(min(imW, (boxes[i][3] * imW)))

            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)

            object_name = labels[int(classes[i])]
            if object_name in ['person', 'knife', 'dog', 'cat', 'bicycle']:
                label = f'{object_name}: {int(scores[i] * 100)}%'
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                label_ymin = max(ymin, labelSize[1] + 10)
                cv2.rectangle(image, (xmin, label_ymin - labelSize[1] - 10),
                              (xmin + labelSize[0], label_ymin + baseLine - 10), (255, 255, 255), cv2.FILLED)
                cv2.putText(image, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                object_found = True
    return object_found
