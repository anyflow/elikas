import os

if "__initialized" not in locals():
    __initialized = True

    TEXT_CYAN = "\033[96m"
    TEXT_RED = "\033[091m"
    TEXT_YELLOW = "\033[1;33m"
    COLOR_OFF = "\033[0m"

    ENVIRONMENT_VARIABLES = [
        "MODE",
    ]

    for variable in ENVIRONMENT_VARIABLES:
        if variable not in os.environ:
            print(
                f"{TEXT_RED}ERROR : {variable} environment variable is not set.{COLOR_OFF}"
            )
            exit(1)

    [
        MODE,
    ] = list(map(os.getenv, ENVIRONMENT_VARIABLES))

    WASMPLUGIN_TEMPLATE_PATH = os.path.join(
        os.path.dirname(__file__), "wasmplugin_template.yaml"
    )
