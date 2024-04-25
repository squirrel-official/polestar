import time
import requests

from picamera2 import Picamera2
from queue import Queue
from customLogging.customLogging import get_logger
from detection.yolov8.objectDetectionYoloV8 import detect_objects
from faceService import facial_comparison_checks

# For writing
UNKNOWN_VISITORS_PATH = '/usr/local/polestar/detections/unknown-visitors/'

VISITOR_NOTIFICATION_URL = 'http://research.local:8087/visitor'
count = 0
logger = get_logger("Motion Detection")

# Queues for captured frames and notification data
frame_queue = Queue()
notification_queue = Queue()


def monitor_camera_stream():
    try:
        # Create a Picamera2 instance
        camera = Picamera2()

        # Configure the still capture stream (no preview)
        config = camera.create_still_configuration(main={"size": (2560, 1440)})
        camera.configure(config)

        # Start the camera stream (without preview)
        camera.start()
        frame_count = 1
        detection_counter = time.time()
        frame_rate = 2  # 2 frames per second
        time_between_captures = 1 / frame_rate
        last_detection_notification_time = time.time();
        max_workers = 2  # Adjust the maximum number of threads as needed
        while True:
            frame = camera.capture_array()
            # Convert YUV frame to RGB for processing
            frame = frame[..., ::-1]
            # Process the frame in a separate thread (non-blocking)
            process_frame(frame, last_detection_notification_time)

            time.sleep(time_between_captures)
            frame_count += 1
    except Exception as e:
        logger.error("An exception occurred in capture thread.")
        logger.error(e, exc_info=True)
        camera.stop()
        camera.close()


def process_frame(image, last_detection_notification_time):
    if detect_objects(image, time.time(), UNKNOWN_VISITORS_PATH):
        if time.time() - last_detection_notification_time > 30:
            print('Sending the Visitor notifications:  {0}', VISITOR_NOTIFICATION_URL)
            # send_notification(VISITOR_NOTIFICATION_URL)
            last_detection_notification_time = time.time()

        facial_comparison_checks(image)


def send_notification(notification_url):
    try:
        data = requests.post(notification_url)
        logger.info("Detected activity sent notification, response : {0}".format(data))
    except Exception as e:
        logger.error("An exception occurred in notification thread.")
        logger.error(e, exc_info=True)


def start_monitoring():
    try:
        monitor_camera_stream()
    except Exception as e:
        logger.error("An exception occurred.")
        logger.error(e, exc_info=True)


start_monitoring()
