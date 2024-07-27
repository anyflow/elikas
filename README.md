
# Elikas

OpenAPI to Istio WasmPlugin, VirtualService converter

## Test commands

```bash
# for dockebi
PYTHONPATH=elikas OPENAPI_PATH=./tests/openapi.dockebi.yaml WASMPLUGIN_PATH=./tests/output.dockebi.yaml python -m elikas
# for public-apigw
PYTHONPATH=elikas OPENAPI_PATH=./tests/openapi.public-apigw.yaml WASMPLUGIN_PATH=./tests/output.public-apigw.yaml python -m elikas
```
