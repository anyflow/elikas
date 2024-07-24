import json
import time
from datetime import datetime

import yaml
from config import COLOR_OFF, TEXT_CYAN, TEXT_RED, TEXT_YELLOW


class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, False)


def to_yaml(content: dict) -> str:
    return yaml.dump(
        content,
        allow_unicode=True,
        Dumper=IndentDumper,
        sort_keys=False,
        default_flow_style=False,
    )


def dump_yaml(content: dict, file_path: str):
    with open(file_path, "w") as file:
        yaml.dump(
            content,
            file,
            allow_unicode=True,
            Dumper=IndentDumper,
            sort_keys=False,
            default_flow_style=False,
        )


def load_yaml(file_path: str) -> dict:
    with open(file_path) as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as error:
            print(f"Error while parsing YAML file: {error}")
            exit(1)


def load_json(file_path: str) -> dict:
    with open(file_path, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError as error:
            print(f"Error while parsing JSON file: {error}")
            exit(1)


def print_yellow(text: str):
    print(f"{TEXT_YELLOW}{text}{COLOR_OFF}", flush=True)


def print_red(text: str):
    print(f"{TEXT_RED}{text}{COLOR_OFF}", flush=True)


def print_cyan(text: str):
    print(f"{TEXT_CYAN}{text}{COLOR_OFF}", flush=True)


def now() -> str:
    return datetime.fromtimestamp(time.time()).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
