from pathlib import Path


HOME_DIR = home = str(Path.home())
CONFIG_DIR_NAME = '.eunice'
CONFIG_FILE_NAME = 'eunice.cfg'
CONFIG_FILE_LOCATION = f"{HOME_DIR}/{CONFIG_DIR_NAME}/{CONFIG_FILE_NAME}"
EUNICE_HOME = f"{HOME_DIR}/{CONFIG_DIR_NAME}"
HOME_DIR_CREATE = f"mkdir {EUNICE_HOME}"
