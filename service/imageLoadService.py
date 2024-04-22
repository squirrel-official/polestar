from deepface import DeepFace
import time
import glob
from customLogging.customLogging import get_logger

count = 0

# For reading
FAMILIAR_FACES_PATH = '/usr/local/polestar/data/familiar-faces/*'
WANTED_CRIMINALS_PATH = '/usr/local/polestar/data/wanted-criminals/*'

logger = get_logger("ImageLoadService")


def load_criminal_images(model):
    criminal_cache = []
    start_date_time = time.time()
    for eachWantedCriminalPath in glob.glob(WANTED_CRIMINALS_PATH):
        try:
            criminal_image = DeepFace.represent(eachWantedCriminalPath, model_name = model)
            # print(criminal_image)
            print(criminal_image[0])
            print(criminal_image[0]['embedding'])
            criminal_cache.append(criminal_image[1][0]['embedding'])
        except Exception as e:
            logger.error("An exception occurred while reading {0}: {1}".format(eachWantedCriminalPath, str(e)))
    logger.info(
        "Loaded {0} criminal images in {1} seconds".format(len(criminal_cache), (time.time() - start_date_time)))
    return criminal_cache


def load_known_images(model):
    known_person_cache = []
    start_date_time = time.time()
    for eachWantedKnownPersonPath in glob.glob(FAMILIAR_FACES_PATH):
        try:
            known_person_image = DeepFace.represent(eachWantedKnownPersonPath, model_name = model)
            known_person_cache.append(known_person_image[1][0]['embedding'])
        except Exception as e:
            logger.error("An exception occurred while reading {0}: {1}".format(eachWantedKnownPersonPath, str(e)))
    logger.info(
        "Loaded {0} known images in {1} seconds".format(len(known_person_cache), (time.time() - start_date_time)))
    return known_person_cache
