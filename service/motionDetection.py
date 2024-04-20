import time
import cv2
import requests

from picamera2 import Picamera2
from queue import Queue
from customLogging.customLogging import get_logger
from detection.yolov8.objectDetectionYoloV8 import detect_objects
from faceService import analyze_face
from imageLoadService import load_criminal_images, load_known_images
from threading import Thread

# Data Models path
ssd_model_path = '/usr/local/polestar/model/coco-ssd-mobilenet'
efficientdet_lite0_path = '/usr/local/polestar/model/efficientdet-lite0/efficientdet_lite0.tflite'

# For writing
UNKNOWN_VISITORS_PATH = '/usr/local/polestar/detections/unknown-visitors/'

NOTIFICATION_URL = 'http://my-security.local:8087/visitor'
count = 0
logger = get_logger("Motion Detection")

# Queues for captured frames and notification data
frame_queue = Queue()
notification_queue = Queue()


def monitor_camera_stream(criminal_cache, known_person_cache):
    try:
        # Create a Picamera2 instance
        camera = Picamera2()

        # Configure the still capture stream (no preview)
        config = camera.create_still_configuration(main={"size": (1024, 768)})
        camera.configure(config)

        # Start the camera stream (without preview)
        camera.start()

        frame_count = 1
        image_count = 1
        object_detection_flag = 0
        detection_counter = time.time()

        while True:
            # Get a frame and metadata from the camera
            frame = camera.capture_array()

            # Convert YUV frame to RGB for processing
            frame = frame[..., ::-1]
            # Process the frame in a separate thread (non-blocking)
            process_frame(frame, criminal_cache, known_person_cache, detection_counter)
            # process_frame_thread = Thread(target=process_frame,
            #                               args=(frame, criminal_cache, known_person_cache))
            # process_frame_thread.start()
            frame_count += 1
    except Exception as e:
        logger.error("An exception occurred in capture thread.")
        logger.error(e, exc_info=True)
        camera.stop()
        camera.close()


def process_frame(image, criminal_cache, known_person_cache, detection_counter):
    object_detection_flag = 0
    print('processing frame')
    if detect_objects(image):
        logger.debug("Object detected, flag :{0}".format(object_detection_flag))
        if object_detection_flag == 0:
            detection_counter = time.time()
            object_detection_flag = 1
        complete_file_name = UNKNOWN_VISITORS_PATH + str(detection_counter) + '.jpg'
        print(complete_file_name)
        cv2.imwrite(complete_file_name, image)
        analyze_face(image,str(detection_counter) , criminal_cache, known_person_cache)

    if (time.time() - detection_counter) > 3 and object_detection_flag == 1:
        object_detection_flag = 0
        # Send notification (non-blocking)
        send_notification(NOTIFICATION_URL)


def send_notification(notification_url):
    try:
        data = requests.post(notification_url)
        logger.info("Detected activity sent notification, response : {0}".format(data))
    except Exception as e:
        logger.error("An exception occurred in notification thread.")
        logger.error(e, exc_info=True)


def start_monitoring():
    try:
        criminal_cache = load_criminal_images()
        known_person_cache = load_known_images()
        p1 = Thread(target=monitor_camera_stream, args=(criminal_cache, known_person_cache,))
        p1.start()
    except Exception as e:
        logger.error("An exception occurred.")
        logger.error(e, exc_info=True)


start_monitoring()
