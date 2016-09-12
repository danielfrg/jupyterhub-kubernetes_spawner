
import os

from . import swagger_client as swagger
from .swagger_client.models.v1_pod import V1Pod
from .swagger_client.models.v1_pod_spec import V1PodSpec
from .swagger_client.models.v1_object_meta import V1ObjectMeta
from .swagger_client.models.v1_container import V1Container
from .swagger_client.models.v1_container_port import V1ContainerPort
from .swagger_client.models.v1_env_var import V1EnvVar
from .swagger_client.models.v1_env_var_source import V1EnvVarSource
from .swagger_client.models.v1_volume import V1Volume
from .swagger_client.models.v1_volume_mount import V1VolumeMount
from .swagger_client.models.v1_persistent_volume_claim_volume_source import V1PersistentVolumeClaimVolumeSource
from .swagger_client.models.v1_object_field_selector import V1ObjectFieldSelector
from .swagger_client.models.v1_resource_requirements import V1ResourceRequirements


class KubernetesClient(object):

    def __init__(self, host, token, verify_ssl=True):
        swagger.Configuration().verify_ssl = verify_ssl
        self.client = swagger.ApiClient(host)
        self.client.default_headers["Authorization"] = token
        self.client.default_headers["Content-Type"] = "application/json"

        self.api = swagger.ApivApi(self.client)
        self.default_namespace = "default"

    @classmethod
    def from_username_password(cls, host, username, password, *args, **kwargs):
        swagger.Configuration().username = username
        swagger.Configuration().password = password
        token = swagger.Configuration().get_basic_auth_token()
        return cls(host, token, *args, **kwargs)

    @classmethod
    def from_service_account(cls, host, *args, **kwargs):
        fpath = "/var/run/secrets/kubernetes.io/serviceaccount/token"
        if not os.path.exists(fpath):
            raise Exception("Token file '{}' not found".format(fpath))
        with open(fpath, "r") as f:
            token = f.read()
        return cls(host, token, *args, **kwargs)

    def launch_pod(self, pod, namespace=None):
        namespace = namespace or self.default_namespace
        self.api.create_namespaced_pod(pod, namespace=namespace)

    def get_pod(self, name, namespace=None):
        namespace = namespace or self.default_namespace
        try:
            return self.api.read_namespaced_pod(name=name, namespace=namespace)
        except swagger.rest.ApiException:
            return None

    def delete_pod(self, name, namespace=None):
        namespace = namespace or self.default_namespace
        self.api.delete_namespaced_pod(name=name, namespace=namespace, body={})

    def get_service(self, name, namespace=None):
        namespace = namespace or self.default_namespace
        return self.api.read_namespaced_service(name=name, namespace=namespace)


class Pod(V1Pod):

    def __init__(self, name, *args, **kwargs):
        super(Pod, self).__init__(*args, **kwargs)
        self.kind = "Pod"
        self.api_version = "v1"
        self.metadata = V1ObjectMeta()
        self.metadata.name = None
        self.metadata.labels = {}
        self.spec = V1PodSpec()
        self.spec.containers = []
        self.spec.volumes = []

        self._name = None
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        self.metadata.name = self._name
        self.add_label("name", name)

    def add_label(self, name, value):
        self.metadata.labels.update({name: value})

    def add_container(self, container):
        self.spec.containers.append(container)

    def add_pvc_volume(self, name, claim_name):
        volume = V1Volume()
        volume.name = name
        pvc_source = V1PersistentVolumeClaimVolumeSource()
        pvc_source.claim_name = claim_name
        volume.persistent_volume_claim = pvc_source
        self.spec.volumes.append(volume)


class Container(V1Container):

    def __init__(self, *args, **kwargs):
        super(Container, self).__init__(*args, **kwargs)
        self.name = "{name}"
        self.ports = []
        self.env = []
        self.volume_mounts = []
        self.add_pod_ip_env()
        self.add_default_resources()

    def add_port(self, port):
        port_ = V1ContainerPort()
        port_.container_port = port
        self.ports.append(port_)

    def add_env(self, name, value):
        env_ = V1EnvVar()
        env_.name = name
        env_.value = value
        self.env.append(env_)

    def add_pod_ip_env(self):
        env_ = V1EnvVar()
        env_.name = "POD_IP"
        field_selector = V1ObjectFieldSelector()
        field_selector.field_path = "status.podIP"
        env_source = V1EnvVarSource()
        env_source.field_ref = field_selector
        env_.value_from = env_source
        self.env.append(env_)

    def add_default_resources(self):
        self.resources = V1ResourceRequirements()
        self.resources.requests = {"cpu": 0.25, "memory": "1Gi"}
        self.resources.limits = {"cpu": 0.25, "memory": "1Gi"}

    def add_volume(self, name, path):
        volume_mount = V1VolumeMount()
        volume_mount.name = name
        volume_mount.mount_path = path
        self.volume_mounts.append(volume_mount)

    def set_command(self, command):
        if isinstance(command, str):
            self.command = command.split(" ")
        if isinstance(command, list):
            self.command = command

class BaseContainer(Container):

    def __init__(self, name, image, *args, **kwargs):
        super(BaseContainer, self).__init__(*args, **kwargs)
        self.name = name
        self.image = image
