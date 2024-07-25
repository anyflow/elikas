from config import OPENAPI_PATH, WASMPLUGIN_PATH, WASMPLUGIN_TEMPLATE
from utilities import dump_yaml, load_yaml


def create_wasmplugin() -> None:
    openapi = __validate(load_yaml(OPENAPI_PATH))

    app = openapi["x-tcn"]["app"]
    namespace = openapi["krakendEndpoint"]["backend"]["host"].split(".")[1]

    wasmplugin = {
        **WASMPLUGIN_TEMPLATE,
        "metadata": {
            "name": f"{app}-endpoint-filter",
            "namespace": namespace,
        },
        "spec": {
            "selector": {"matchLabels": {"app": app}},
            **WASMPLUGIN_TEMPLATE.get("spec", {}),
        },
    }

    dump_yaml(wasmplugin, WASMPLUGIN_PATH)
    return


def __validate(openapi: dict) -> dict:
    # TODO: Validate OpenAPI
    return openapi
