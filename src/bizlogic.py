from config import ENVIRIONMENT
from utilities import now, print_cyan, print_red, print_yellow


def convert() -> str:
    print_yellow("convert")
    print_cyan("convert")
    print_red("convert")
    return f"convert {ENVIRIONMENT} {now()}"
