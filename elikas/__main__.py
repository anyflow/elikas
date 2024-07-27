import argparse
import os

import bizlogic
from config import COLOR_OFF, ENVIRONMENT_VARIABLES, TEXT_RED


def main(args):
    for variable in ENVIRONMENT_VARIABLES:
        if variable not in os.environ:
            print(
                f"{TEXT_RED}ERROR : {variable} environment variable is not set.{COLOR_OFF}"
            )
            exit(1)

    bizlogic.create_from_tcn_openapi()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="elikas")
    subparsers = parser.add_subparsers()

    main(parser.parse_args())
