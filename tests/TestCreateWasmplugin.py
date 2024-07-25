import unittest
from unittest.mock import MagicMock, patch

from elikas.bizlogic import create_wasmplugin
from elikas.config import WASMPLUGIN_TEMPLATE


class TestCreateWasmplugin(unittest.TestCase):

    @patch("my_module.load_yaml")
    @patch("my_module.__validate")
    @patch("my_module.dump_yaml")
    def test_create_wasmplugin(self, mock_dump_yaml, mock_validate, mock_load_yaml):
        mock_load_yaml.return_value = {
            "x-tcn": {
                "app": "my-app",
            },
            "krakendEndpoint": {
                "backend": {
                    "host": "api.my-namespace.com",
                },
            },
        }

        create_wasmplugin()

        mock_load_yaml.assert_called_once_with("OPENAPI_PATH")
        mock_validate.assert_called_once_with(mock_load_yaml.return_value)
        mock_dump_yaml.assert_called_once_with(
            {
                **WASMPLUGIN_TEMPLATE,
                "metadata": {
                    "name": "my-app-endpoint-filter",
                    "namespace": "my-namespace",
                },
                "spec": {
                    "selector": {"matchLabels": {"app": "my-app"}},
                    **WASMPLUGIN_TEMPLATE.get("spec", {}),
                },
            },
            "WASMPLUGIN_PATH",
        )
