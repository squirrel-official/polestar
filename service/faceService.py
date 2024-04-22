from customLogging.customLogging import get_logger
from deepface import DeepFace

logger = get_logger("FaceComparisonUtil")
MOTION_VIDEO_URL = '/var/lib/motion/*'
CONFIG_PROPERTIES = '/usr/local/polestar/config.properties'
ARCHIVE_URL = "/usr/local/polestar/data/archives/"

# For writing
UNKNOWN_VISITORS_PATH = '/usr/local/polestar/result/unknown-visitors/'
CAPTURED_CRIMINALS_PATH = '/usr/local/polestar/result/captured-criminals/'
KNOWN_VISITORS_PATH = '/usr/local/polestar/result/known-visitors/'

# For reading
FAMILIAR_FACES_PATH = '/usr/local/polestar/data/familiar-faces/*'
WANTED_CRIMINALS_PATH = '/usr/local/polestar/data/wanted-criminals/*'

CRIMINAL_NOTIFICATION_URL = 'http://my-security.local:8087/criminal'
VISITOR_NOTIFICATION_URL = 'http://my-security.local:8087/visitor'
FRIEND_NOTIFICATION_URL = 'http://my-security.local:8087/friend'


def facial_comparison_checks(image, criminal_cache, known_person_cache, model):
    unknown_faces = DeepFace.extract_faces(image, enforce_detection=False)
    if unknown_faces is not None:
        logger.debug('A new person identified by face so processing it')
        for unknown_face in enumerate(unknown_faces):
            for criminal_face_encoding in enumerate(criminal_cache):
                # face tuple's 2nd  element has facial encodings
                unknown_face_encoding = unknown_face[1]['face']
                result = DeepFace.verify(unknown_face_encoding, criminal_face_encoding[1], enforce_detection=False,
                                         model_name=model)
                # result = DeepFace.verify(unknown_face_encoding, unknown_face_encoding,enforce_detection=False)
                face_match = result["verified"]
                if face_match:
                    return True

            for each_known_person_encoding in known_person_cache:
                result = DeepFace.verify(unknown_face_encoding, each_known_person_encoding[1], enforce_detection=False,
                                         model_name=model)
                print(result["verified"])


def extract_unknown_face_encodings(unknown_image, model):
    # Detect faces in the unknown image
    unknown_faces = DeepFace.detectFace(unknown_image, enforce_detection=True, model_name=model)

    # Initialize a list to store unknown face encodings
    unknown_face_encoding_list = []

    # Iterate through each detected face in the unknown image
    for unknown_face in unknown_faces:
        # Calculate the encoding for the detected face
        unknown_face_encoding = DeepFace.represent(unknown_face, enforce_detection=True, model_name=model)
        # Append the encoding to the list
        unknown_face_encoding_list.append(unknown_face_encoding)

    # Return the list of unknown face encodings
    return unknown_face_encoding_list



