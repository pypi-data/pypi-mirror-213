import os
import subprocess

from kubernetes import client
from kubernetes import config


# Create DriverlessAISetup objects.
def create_dai_setups(namespace: str) -> None:
    dai_setups_dir_path = os.path.join(
        os.path.dirname(__file__), "test_data", "dai_setups"
    )

    # Cannot use kubernetes library because it does not support similar functionality
    # as "kubectl apply" for CRDs (https://github.com/kubernetes-client/python/issues/740).
    # Need to run the command directly via subprocess.
    subprocess.run(
        [
            "kubectl",
            "apply",
            "-f",
            dai_setups_dir_path,
            "--recursive",
            f"--namespace={namespace}",
        ],
        check=True,
    )


# Create H2OSetup objects.
def create_h2o_setups(namespace: str) -> None:
    h2o_setups_dir_path = os.path.join(
        os.path.dirname(__file__), "test_data", "h2o_setups"
    )

    # Cannot use kubernetes library because it does not support similar functionality
    # as "kubectl apply" for CRDs (https://github.com/kubernetes-client/python/issues/740).
    # Need to run the command directly via subprocess.
    subprocess.run(
        [
            "kubectl",
            "apply",
            "-f",
            h2o_setups_dir_path,
            "--recursive",
            f"--namespace={namespace}",
        ],
        check=True,
    )


# Create DAIEngine license.
def create_dai_license(namespace: str) -> None:
    data = {"license.sig": os.getenv("DAI_LICENSE")}
    body = client.V1Secret(
        metadata=client.V1ObjectMeta(name="dai-license"),
        type="Opaque",
        string_data=data,
    )
    client.CoreV1Api().create_namespaced_secret(namespace=namespace, body=body)


# Create DAIVersion CRDs.
def create_dai_versions(namespace: str) -> None:
    dai_versions_dir_path = os.path.join(
        os.path.dirname(__file__), "test_data", "dai_versions"
    )

    # Cannot use kubernetes library because it does not support similar functionality
    # as "kubectl apply" for CRDs (https://github.com/kubernetes-client/python/issues/740).
    # Need to run the command directly via subprocess.
    subprocess.run(
        [
            "kubectl",
            "apply",
            "-f",
            dai_versions_dir_path,
            "--recursive",
            f"--namespace={namespace}",
        ]
    )


# Create H2OVersions.
def create_h2o_versions(namespace: str) -> None:
    h2o_versions_dir_path = os.path.join(
        os.path.dirname(__file__), "test_data", "h2o_versions"
    )

    # Cannot use kubernetes library because it does not support similar functionality
    # as "kubectl apply" for CRDs (https://github.com/kubernetes-client/python/issues/740).
    # Need to run the command directly via subprocess.
    subprocess.run(
        [
            "kubectl",
            "apply",
            "-f",
            h2o_versions_dir_path,
            "--recursive",
            f"--namespace={namespace}",
        ]
    )


def setup_mlops_secrets(namespace: str) -> None:
    # Gather data from existing secrets.
    ca_secret = client.CoreV1Api().read_namespaced_secret(
        "hac-mlops-dev-ca", "mlops-dev"
    )
    ca_cert = ca_secret.data["certificate"]

    client_secret = client.CoreV1Api().read_namespaced_secret(
        "hac-mlops-dev-driverless-tls-client", "mlops-dev"
    )
    client_cert = client_secret.data["certificate"]
    client_key = client_secret.data["key"]

    client.CoreV1Api().create_namespaced_secret(
        namespace,
        client.V1Secret(
            metadata=client.V1ObjectMeta(
                name=ca_secret.metadata.name, labels=ca_secret.metadata.labels
            ),
            data={"tls.crt": ca_cert},
        ),
    )

    client.CoreV1Api().create_namespaced_secret(
        namespace,
        client.V1Secret(
            metadata=client.V1ObjectMeta(
                name=client_secret.metadata.name, labels=client_secret.metadata.labels
            ),
            data={"tls.crt": client_cert, "tls.key": client_key},
        ),
    )


config.load_config()
system_namespace = os.getenv("TEST_K8S_SYSTEM_NAMESPACE")
create_dai_versions(namespace=system_namespace)
create_h2o_versions(namespace=system_namespace)
create_dai_setups(namespace=system_namespace)
create_h2o_setups(namespace=system_namespace)
create_dai_license(namespace=system_namespace)

if os.getenv("HAIC_CLUSTER") == "true":
    setup_mlops_secrets(namespace=system_namespace)
