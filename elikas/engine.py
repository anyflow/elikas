import os
import re

from config import WASMPLUGIN_TEMPLATE_PATH
from utilities import load_yaml

[
    OPENAPI_PATH,
    WASMPLUGIN_PATH,
] = list(map(os.getenv, ["OPENAPI_PATH", "WASMPLUGIN_PATH"]))


def create(app: str, namespace: str, openapi_paths: list) -> dict:
    template = load_yaml(WASMPLUGIN_TEMPLATE_PATH)
    seen = set()

    return {
        **template,
        "metadata": {
            "name": f"{app}-endpoint-metric-filter",
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
                            for path in openapi_paths
                            if str(item := __request_apigroup_item(path)) not in seen
                            and not seen.add(str(item))
                        ],
                    },
                    {
                        "output_attribute": "request_path",
                        "match": [__request_path_item(path) for path in openapi_paths],
                    },
                ],
            },
        },
    }


def validate(openapi: dict) -> dict:
    # TODO: Validate OpenAPI
    return openapi


def __request_path_item(path):
    if "{" in path:
        pattern = re.sub(r"\{([^}]+)\}", r"^[A-Za-z0-9_.-]*$", path)
        # pattern = re.sub(r"\{([^}]+)\}", r"^[:alnum:]*$", path)
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
            f"^{match.groups()[1]}/.*$" if match.groups()[2] else f"{match.groups()[1]}"
        )
        return {
            "value": match.groups()[1],
            "condition": f"request.url_path.matches('{pattern}')",
        }
    else:
        apigroup = path.split("/")[1]
        return {
            "value": apigroup,
            "condition": f"request.url_path.matches('^/{apigroup}/.*$')",
        }
