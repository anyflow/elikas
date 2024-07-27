import os

import engine
from utilities import dump_yaml, load_yaml, wrap_values_and_conditions

[
    OPENAPI_PATH,
    WASMPLUGIN_PATH,
] = list(map(os.getenv, ["OPENAPI_PATH", "WASMPLUGIN_PATH"]))


def create() -> None:
    openapi = engine.validate(load_yaml(OPENAPI_PATH))

    wasmplugin = engine.create(
        openapi["x-tcn"]["app"],
        openapi["x-tcn"]["krakendEndpoint"]["backend"]["host"].split(".")[1],
        openapi.get("paths", {}).keys(),
    )

    dump_yaml(wasmplugin, WASMPLUGIN_PATH)
    wrap_values_and_conditions(WASMPLUGIN_PATH)
    return
