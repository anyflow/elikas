import re

from config import OPENAPI_PATH, WASMPLUGIN_PATH, WASMPLUGIN_TEMPLATE_PATH
from utilities import dump_yaml, load_yaml, wrap_values_and_conditions


def create_wasmplugin() -> None:
    openapi = __validate(load_yaml(OPENAPI_PATH))
    app = openapi["x-tcn"]["app"]
    namespace = openapi["x-tcn"]["krakendEndpoint"]["backend"]["host"].split(".")[1]
    paths = openapi.get("paths", {}).keys()

    template = load_yaml(WASMPLUGIN_TEMPLATE_PATH)

    seen = set()
    wasmplugin = {
        **template,
        "metadata": {
            "name": f"{app}-endpoint-filter",
            "namespace": namespace,
        },
        "spec": {
            **template.get("spec", {}),
            "selector": {"matchLabels": {"app": app}},
            "pluginConfig": {
                "attributes": [
                    {
                        "output_attribute": "request_apigroup",
                        "match": [
                            item
                            for path in paths
                            if str(item := __request_apigroup_item(path)) not in seen
                            and not seen.add(str(item))
                        ],
                    },
                    {
                        "output_attribute": "request_path",
                        "match": [__request_path_item(path) for path in paths],
                    },
                ],
            },
        },
    }

    dump_yaml(wasmplugin, WASMPLUGIN_PATH)
    wrap_values_and_conditions(WASMPLUGIN_PATH)
    return


def __validate(openapi: dict) -> dict:
    # TODO: Validate OpenAPI
    return openapi


def __request_path_item(path):
    if "{" in path:
        pattern = re.sub(r"\{([^}]+)\}", r"[A-Za-z0-9_.-]*", path)
        condition = f"request.url_path.matches('{pattern}')"
    else:
        condition = f"request.url_path == '{path}'"

    return {
        "value": path,
        "condition": condition,
    }


def __request_apigroup_item(path):
    if match := re.match(r"^\/(v[0-9]+)\/([^\/]+)(?:\/([^\/]+))*$", path):
        pattern = "/v[0-9]+/" + (
            f"{match.groups()[1]}/.*" if match.groups()[2] else f"{match.groups()[1]}"
        )
        return {
            "value": match.groups()[1],
            "condition": f"request.url_path.matches('{pattern}')",
        }
    else:
        apigroup = path.split("/")[1]
        return {
            "value": apigroup,
            "condition": f"request.url_path.matches('/{apigroup}/.*')",
        }
