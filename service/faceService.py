import time
import numpy as np
from customLogging.customLogging import get_logger
from PIL import Image
import cv2
from deepface import DeepFace
import requests

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


def facial_comparison_checks(image, criminal_cache, known_person_cache):
    unknown_faces = DeepFace.extract_faces(image, enforce_detection=False)
    if unknown_faces is not None:
        logger.debug('A new person identified by face so processing it')
        for face in enumerate(unknown_faces):
            for each_criminal in criminal_cache:
                print(face)
                print(face[0])
                print(face[0]["face"])
                print(type(face))
                print(type(each_criminal))
                result = DeepFace.verify(face, each_criminal)
                # result = DeepFace.verify(face, face)
                print(result)
                print(result["verified"])

            for each_known_person in known_person_cache:
                result = DeepFace.verify(face, each_known_person)
                print(result)
                print(result["verified"])


def extract_unknown_face_encodings(unknown_image):
    # Detect faces in the unknown image
    unknown_faces = DeepFace.detectFace(unknown_image, enforce_detection=True)

    # Initialize a list to store unknown face encodings
    unknown_face_encoding_list = []

    # Iterate through each detected face in the unknown image
    for unknown_face in unknown_faces:
        # Calculate the encoding for the detected face
        unknown_face_encoding = DeepFace.represent(unknown_face, enforce_detection=True)
        # Append the encoding to the list
        unknown_face_encoding_list.append(unknown_face_encoding)

    # Return the list of unknown face encodings
    return unknown_face_encoding_list


def compare_faces_with_encodings(known_image_encoding, unknown_image_encoding_list, each_wanted_criminal_path):
    # Iterate through each unknown face encoding
    for each_unknown_face_encoding in unknown_image_encoding_list:
        # Compare the unknown face encoding with the known face encoding
        result = DeepFace.verify(known_image_encoding, each_unknown_face_encoding)
        # If the faces match, print a message and return True
        if result["verified"]:
            print(f"Face comparison match with {each_wanted_criminal_path}")
            return True

    # If no matching faces are found, return False
    return False


def compare_faces_with_path(known_image_path, unknown_image_path):
    # Load known image and encode the face
    known_face = DeepFace.detectFace(known_image_path, enforce_detection=True)
    known_encoding = DeepFace.represent(known_face, enforce_detection=True)

    # Load unknown image and detect faces
    unknown_faces = DeepFace.detectFace(unknown_image_path, enforce_detection=True)

    # Iterate through each detected face in the unknown image
    for unknown_face in unknown_faces:
        # Compare the unknown face with the known face
        result = DeepFace.verify(known_encoding, unknown_face)
        # If the faces match, return True
        if result["verified"]:
            return True

    # If no matching faces are found, return False
    return False
