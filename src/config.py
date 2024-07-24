import os

if "__initialized" not in locals():
    __initialized = True

    TEXT_CYAN = "\033[96m"
    TEXT_RED = "\033[091m"
    TEXT_YELLOW = "\033[1;33m"
    COLOR_OFF = "\033[0m"

    ENVIRONMENT_VARIABLES = [
        "ENVIRONMENT",
    ]

    [
        ENVIRONMENT,
    ] = list(map(os.getenv, ENVIRONMENT_VARIABLES))
