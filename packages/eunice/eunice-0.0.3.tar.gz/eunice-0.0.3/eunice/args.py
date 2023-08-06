import argparse


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Eunice - CLI wrapper for ChatGPT"
    )
    parser.add_argument(
        "-l",
        "--log",
        help="Set the log level",
        type=str,
        choices=[
            "DEBUG",
            "INFO",
        ],
    )
    return parser.parse_args()
