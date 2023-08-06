from eunice.run import ask
from eunice.models import Config
from eunice.args import get_arguments
from eunice.eunice_logging import logging_config


config = Config()

def main():
    args = get_arguments()
    logging_config(args.log)
    ask(config)


if __name__ == '__main__':
    main()
