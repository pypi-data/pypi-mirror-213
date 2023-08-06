from dataclasses import dataclass
import logging
import tomli
from eunice.definitions import CONFIG_FILE_LOCATION
from eunice.utils import check_for_file

logger = logging.getLogger(__name__)
  

@dataclass
class Config:
    openai_secret_key=None


class ConfigFile:
    def __init__(self):
        self.config_file = CONFIG_FILE_LOCATION
        self.is_config = check_for_file(self.config_file)


    def load_config(self):
        with open(self.config_file, mode='rb') as f:
            return tomli.load(f)

    def set_config(self, config: Config):

        if self.is_config is True:
            config_file = self.load_config()
            logger.info(config_file)
            try:
                general = config_file["general"]
                try:
                    config.openai_secret_key = general["openai_secret_key"]
                    logger.info(f"CONFIG: Found openai secret key!")
                except KeyError as k:
                    print("CONFIG ERROR: Missing OpenAI Secret Key")
                
            except KeyError as k:
                logger.info(k)
                pass
