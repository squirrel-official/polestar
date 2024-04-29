import time

import requests
import numpy as np

from customLogging.customLogging import get_logger
from deepface import DeepFace
from PIL import Image

logger = get_logger("FaceComparisonUtil")
MOTION_VIDEO_URL = '/var/lib/motion/*'
CONFIG_PROPERTIES = '/usr/local/polestar/config.properties'
ARCHIVE_URL = "/usr/local/polestar/data/archives/"

# For reading
WANTED_CRIMINALS_PATH = '/usr/local/polestar/data/wanted-criminals/'
FAMILIAR_FACES_PATH = '/usr/local/polestar/data/familiar-faces/'

CRIMINAL_SAVE_PATH = '/usr/local/polestar/detections/captured-criminals/'
FAMILIAR_SAVE_PATH = '/usr/local/polestar/detections/familiar-faces/'

CRIMINAL_NOTIFICATION_URL = 'http://research.local:8087/criminal'
FRIEND_NOTIFICATION_URL = 'http://research.local:8087/friend'


def facial_comparison_checks(image):
    detectors = ["opencv", "ssd", "mtcnn", "dlib", "retinaface"]
    backends = ['opencv', 'ssd', 'yolov8']
    try:
        start_time = time.time()
        unknown_faces = DeepFace.extract_faces(image, enforce_detection=True, detector_backend=backends[2])
        if unknown_faces is not None:
            logger.debug('face extraction success , total time : ' + str((time.time() - start_time)))
            for unknown_face in enumerate(unknown_faces):
                # face tuple's 2nd  element has facial encodings
                unknown_face_encoding = unknown_face[1]['face']
                im = Image.fromarray((unknown_face_encoding * 255).astype(np.uint8))
                im.save('/usr/local/polestar/detections/unknown-visitors/face' + str(time.time()) + '.jpeg')
                criminal_result = DeepFace.find(img_path=unknown_face_encoding,
                                                db_path=WANTED_CRIMINALS_PATH, enforce_detection=True,
                                                detector_backend=backends[2], silent=False)
                print(criminal_result)
                if criminal_result is not None and len(criminal_result) > 0:
                    print('Suspected criminal found, triggering notification')
                    image.save_as_jpeg(CRIMINAL_SAVE_PATH + str(time.time()) + '.jpeg')
                    send_notification(CRIMINAL_NOTIFICATION_URL)
                    return True

                friend_result = DeepFace.find(img_path=unknown_face_encoding,
                                              db_path=FAMILIAR_FACES_PATH, enforce_detection=True,
                                              detector_backend=backends[2], silent=True)
                print(friend_result)
                if friend_result is not None and len(friend_result) > 0:
                    print('Friend/family guests found, triggering notification')
                    image.save_as_jpeg(FAMILIAR_SAVE_PATH + str(time.time()) + '.jpeg')
                    send_notification(FRIEND_NOTIFICATION_URL)
                    return True

    except Exception as e:
        logger.error(e)
        pass


def send_notification(notification_url):
    try:
        data = requests.post(notification_url)
        logger.info("Detected activity sent notification, response : {0}".format(data))
    except Exception as e:
        logger.error("An exception occurred in notification thread.")
        logger.error(e, exc_info=True)
