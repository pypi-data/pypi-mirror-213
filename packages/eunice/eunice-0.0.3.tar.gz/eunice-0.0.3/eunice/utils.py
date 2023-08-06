import os
import logging


logger = logging.getLogger(__name__)


def check_for_dir(path):
    is_dir = os.path.isdir(path)
    logger.info(f"check_for_dir {path} {is_dir}")
    return is_dir

def check_for_file(path):
    is_file = os.path.isfile(path)
    logger.info(f"check_for_file {path} {is_file}")
    return is_file
