import argparse
import os

import bizlogic
import config
from utilities import COLOR_OFF, TEXT_RED


def main(args):
    for variable in config.ENVIRONMENT_VARIABLES:
        if variable not in os.environ:
            print(
                f"{TEXT_RED}ERROR : {variable} environment variable is not set.{COLOR_OFF}"
            )
            exit(1)

    match args.command:
        case "test":
            bizlogic.test(args.color, args.target_version, args.base_version)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="elikas")
    subparsers = parser.add_subparsers()

    parser.add_argument(
        "-c",
        "--command",
        choices=[
            "test",
        ],
        required=True,
        help="Select a command",
    )

    main(parser.parse_args())
