import cv2
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

CRIMINAL_NOTIFICATION_URL = 'http://my-security.local:8087/criminal'
VISITOR_NOTIFICATION_URL = 'http://my-security.local:8087/visitor'
FRIEND_NOTIFICATION_URL = 'http://my-security.local:8087/friend'


def facial_comparison_checks(image):
    detectors = ["opencv", "ssd", "mtcnn", "dlib", "retinaface"]
    try:
        unknown_faces = DeepFace.extract_faces(image, enforce_detection=True)
        if unknown_faces is not None:
            logger.debug('A new person identified by face so processing it')
            for unknown_face in enumerate(unknown_faces):
                # face tuple's 2nd  element has facial encodings
                unknown_face_encoding = unknown_face[1]['face']
                immgg = cv2.normalize(unknown_face_encoding, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX,
                                      dtype=cv2.CV_8U)
                cv2.imwrite('/usr/local/polestar/detections/unknown-visitors/face.jpeg', immgg)
                print('anil')
                im = Image.fromarray((unknown_face_encoding * 255).astype(np.uint8))
                im.save('/usr/local/polestar/detections/unknown-visitors/face1.jpeg')

                criminal_result = DeepFace.find(img_path=unknown_face_encoding,
                                                db_path=WANTED_CRIMINALS_PATH, enforce_detection=False)
                print(criminal_result)

                friend_result = DeepFace.find(img_path=unknown_face_encoding,
                                              db_path=FAMILIAR_FACES_PATH, enforce_detection=False)
                print(friend_result)
    except Exception as e:
        logger.error(e)
        logger.info('Unable to extract the face from passed frame')
        pass
