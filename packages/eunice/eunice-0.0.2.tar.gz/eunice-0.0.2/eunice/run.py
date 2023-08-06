import openai
import sys
import subprocess
import logging
from eunice.models import Config, ConfigFile
from eunice.definitions import HOME_DIR_CREATE, EUNICE_HOME
from eunice.utils import check_for_dir

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


logger = logging.getLogger(__name__)

def config_allocation(config):
    config_file = ConfigFile()
    config_file.set_config(config)

def run_subprocess(script: str):
    if "rm " in script:
        sys.exit()
    try:
        subprocess.run(script, shell=True, check=True, timeout=30)
    except subprocess.CalledProcessError as e:
        logger.error(e)

def virgin_boostrap():
    global initial_boot_flag
    initial_boot_flag = True
    logger.info("First boot")
    run_subprocess(HOME_DIR_CREATE)

def chat_create(message_history: list[dict]):
    return openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=message_history)

def ask(config: Config):

    if check_for_dir(EUNICE_HOME) is False:
        virgin_boostrap()

    config_allocation(config)
    openai.api_key = config.openai_secret_key

    print(bcolors.WARNING + "Calling Eunice, please wait..." + bcolors.ENDC)

    message_history = []

    prep_for_nan = {"role": "system", "content": "You are a friendly assistance called Eunice."}
    message_history.append(prep_for_nan)
    
    print(bcolors.OKGREEN + "p(*＾ -＾ *)q" + bcolors.ENDC)
    print(bcolors.OKGREEN + "Hello dear, please speak up" + bcolors.ENDC)
    while True:
        user_chat = input(bcolors.OKCYAN + "You: " + bcolors.ENDC)
        assemble_message = {"role": "system", "content": user_chat}
        message_history.append(assemble_message)
        chat_completion = chat_create(message_history)
        print(bcolors.OKGREEN + chat_completion.choices[0].message.content + bcolors.ENDC)

