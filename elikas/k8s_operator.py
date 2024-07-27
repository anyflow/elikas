import engine
import kopf
import kubernetes
from kubernetes.client.rest import ApiException


# Define the Kubernetes client
def run():
    kopf.run()


def custom_api():
    kubernetes.config.load_kube_config()
    api_client = kubernetes.client.ApiClient()

    return kubernetes.client.CustomObjectsApi(api_client)


@kopf.on.create("elikas.io", "v1alpha1", "elikas")
def create_fn(spec, name, namespace, **kwargs):
    kopf.info(f"Creating Elikas: {name} in namespace: {namespace}")

    openapi_spec = engine.validate(spec.get("openapi"))
    if openapi_spec:
        kopf.info(f"OpenAPI Spec: {openapi_spec}")
    else:
        kopf.info(f"No OpenAPI Spec provided for {name}")

    wasmplugin = engine.create(
        openapi_spec["selector"]["matchLabels"]["app"],
        openapi_spec["selector"]["matchNamespace"],
        openapi_spec["paths"],
    )

    try:
        custom_api().create_namespaced_custom_object(
            group="extensions.istio.io",
            version="v1alpha1",
            name=name,
            namespace=namespace,
            plural="wasmplugins",
            body=wasmplugin,
        )
        kopf.info(f"WasmPlugin {wasmplugin['metadata']['name']} created successfully.")
    except ApiException as e:
        if e.status == 409:
            kopf.info(
                f"WasmPlugin {wasmplugin['metadata']['name']} already exists. Updating..."
            )
            custom_api.patch_namespaced_custom_object(
                group="extensions.istio.io",
                version="v1alpha1",
                name=name,
                namespace=namespace,
                plural="wasmplugins",
                body=wasmplugin,
            )
            kopf.info(
                f"WasmPlugin {wasmplugin['metadata']['name']} updated successfully."
            )
        else:
            raise

    return {"message": f"Elikas {name} created successfully and WasmPlugin applied."}


@kopf.on.update("elikas.io", "v1alpha1", "elikas")
def update_fn(spec, name, namespace, **kwargs):
    kopf.info(f"Updating Elikas: {name} in namespace: {namespace}")

    openapi_spec = engine.validate(spec.get("openapi"))
    if openapi_spec:
        kopf.info(f"Updated OpenAPI Spec: {openapi_spec}")
    else:
        kopf.info(f"No OpenAPI Spec provided for {name}")

    wasmplugin = engine.create(
        openapi_spec["selector"]["matchLabels"]["app"],
        openapi_spec["selector"]["matchNamespace"],
        openapi_spec["paths"],
    )

    try:
        custom_api().patch_namespaced_custom_object(
            group="extensions.istio.io",
            version="v1alpha1",
            name=name,
            namespace=namespace,
            plural="wasmplugins",
            body=wasmplugin,
        )
        kopf.info(f"WasmPlugin {wasmplugin['metadata']['name']} updated successfully.")
    except ApiException as e:
        raise kopf.TemporaryError(f"Failed to update WasmPlugin: {e}", delay=30)

    return {"message": f"Elikas {name} updated successfully and WasmPlugin applied."}


@kopf.on.delete("elikas.io", "v1alpha1", "elikas")
def delete_fn(spec, name, namespace, **kwargs):
    kopf.info(f"Deleting Elikas: {name} in namespace: {namespace}")

    try:
        custom_api().delete_namespaced_custom_object(
            group="extensions.istio.io",
            version="v1alpha1",
            name=name,
            namespace=namespace,
            plural="wasmplugins",
        )
        kopf.info(f"WasmPlugin {name} deleted successfully.")
    except ApiException as e:
        if e.status == 404:
            kopf.info(f"WasmPlugin {name} not found. Skipping deletion.")
        else:
            raise kopf.TemporaryError(f"Failed to delete WasmPlugin: {e}", delay=30)

    return {"message": f"Elikas {name} deleted successfully and WasmPlugin removed."}
