import string
from textwrap import dedent

from tornado import gen
from escapism import escape
from jupyterhub.spawner import Spawner
from traitlets import Unicode, Bool, Int

from .kube import KubernetesClient, Pod, BaseContainer


class KubernetesSpawner(Spawner):

    host = Unicode("https://kubernetes", config=True, help="Kubernetes HTTP/REST API host")
    username = Unicode("", config=True, help="Kubernetes HTTP/REST API username")
    password = Unicode("", config=True, help="Kubernetes HTTP/REST API password")
    verify_ssl = Bool(True, config=True, help="Kubernetes HTTP/REST API use ssl")

    pod_name_prefix = Unicode(
        "jupyterhub",
        config=True,
        help=dedent(
            """
            Prefix for container names.
            The full container name for a particular user will be: <prefix>-<username>
            """
        )
    )

    container_image = Unicode("jupyterhub/singleuser", config=True)
    container_port = Int(8888, config=True)
    _container_safe_chars = set(string.ascii_letters + string.digits + '-')
    _container_escape_char = '_'

    persistent_volume_claim_name = Unicode(
        "",
        config=True,
        help=dedent(
            """
            The name of the Kubernetes Persistent Volume Claim object
            that will be used to persit the notebooks of all the users
            """
        )
    )

    persistent_volume_claim_path = Unicode(
        "/mnt",
        config=True,
        help=dedent(
            """
            Where to mount the persistent volume claim in the container
            """
        )
    )

    hub_ip = Unicode(
        "",
        config=True,
        help=dedent(
            """
            The Jupyter Hub (Proxy) main IP address.

            This disables hub_ip_from_service
            """
        )
    )

    hub_ip_from_service = Unicode(
        "jupyterhub",
        config=True,
        help=dedent(
            """
            Kubernetes service name to get proxy IP.
            This is useful when running in Kubernetes to make all the pod containers use
            the public facing (load balanced) proxy API IP.
            """
        )
    )

    _client = None

    @property
    def client(self):
        cls = self.__class__
        if cls._client is None:
            if self.verify_ssl is False:
                import requests
                requests.packages.urllib3.disable_warnings()
                import urllib3
                urllib3.disable_warnings()

            if self.username and self.password:
                self.log.debug("Creating Kubernetes client from username and password")
                cls._client = KubernetesClient.from_username_password(self.host, self.username, self.password,
                                                                      verify_ssl=self.verify_ssl)
            else:
                self.log.debug("Creating Kubernetes client from Service Account")
                cls._client = KubernetesClient.from_service_account(self.host, verify_ssl=self.verify_ssl)
        return cls._client

    @gen.coroutine
    def start(self):
        # TODO: handle stoped
        self.log.debug("Starting pod '%s'", self.pod_name)
        pod = self.get_pod()

        if pod is None:
            self.log.debug("Pod '%s' NOT found. Creating it...", self.pod_name)

            new_pod = Pod(name=self.pod_name)

            # Create Jupyter container
            container = BaseContainer(name='jupyter', image=self.container_image)
            container.add_port(self.container_port)
            for env_name, env_value in self.get_env_vars().items():
                container.add_env(env_name, env_value)
            # Mount volume to persist notebooks
            if self.persistent_volume_claim_name and self.persistent_volume_claim_path:
                vol_name = "notebooks"
                new_pod.add_pvc_volume(vol_name, self.persistent_volume_claim_name)
                volume_path = self.persistent_volume_claim_path
                if '{username}' in volume_path:
                    volume_path = volume_path.format(username=self.user.name)
                container.add_volume(vol_name, volume_path)

            new_pod.add_container(container)

            self.client.launch_pod(new_pod)
            pod = yield self.wait_for_new_pod()
        else:
            self.log.debug("Pod '%s' FOUND", self.pod_name)

        ip = pod.status.pod_ip
        self.log.debug("Pod ready at '%s:%s'", ip, self.container_port)

        self.user.server.ip = ip
        self.user.server.port = self.container_port
        return ip, self.container_port

    def get_pod(self):
        return self.client.get_pod(self.pod_name)

    @property
    def pod_name(self):
        return "{}-{}".format(self.pod_name_prefix, self.escaped_name)

    @property
    def escaped_name(self):
        return escape(self.user.name,
                      safe=self._container_safe_chars,
                      escape_char=self._container_escape_char,
                      )

    def get_env_vars(self):
        env = super(KubernetesSpawner, self).get_env()
        ret = {}
        ret['JPY_API_TOKEN'] = env['JPY_API_TOKEN']
        ret['JPY_USER'] = self.user.name
        ret['JPY_COOKIE_NAME'] = self.user.server.cookie_name
        ret['JPY_BASE_URL'] = self.user.server.base_url
        ret['JPY_HUB_PREFIX'] = self.hub.server.base_url
        ret['JPY_HUB_API_URL'] = self._hub_api_url()
        if self.notebook_dir:
            self.notebook_dir = self.notebook_dir.replace("%U", self.user.name)
            self.notebook_dir = self.notebook_dir.replace("{username}", self.user.name)
            ret['NOTEBOOK_DIR'] = self.notebook_dir
        return ret

    def _hub_api_url(self):
        if self.hub_ip:
            ip = self.hub_ip
        if self.hub_ip_from_service:
            api_service = self.client.get_service(self.hub_ip_from_service)
            ip = api_service.status.load_balancer.ingress[0].ip
        else:
            return self.hub.api_url

        proto, path = self.hub.api_url.split('://', 1)
        _ip, rest = path.split(':', 1)
        port, rest = rest.split('/', 1)
        return '{proto}://{ip}/{rest}'.format(proto=proto, ip=ip, rest=rest)

    @gen.coroutine
    def wait_for_new_pod(self):
        self.log.debug("Waiting for new pod '%s' to be 'RUNNING'", self.pod_name)
        while True:
            pod = self.get_pod()
            if pod.status.phase == 'Running':
                self.log.debug("Pod '%s' is finally running", self.pod_name)
                return pod
            elif pod.status.phase in ('Failed', 'Unknown'):
                raise Exception('Couldn\'t launch pod :(')
            elif pod.status.phase in ('Pending',):
                yield gen.sleep(5)

    @gen.coroutine
    def poll(self):
        created_pod = self.get_pod()
        if created_pod is not None and created_pod.status.phase in ('Running',):
            self.log.debug("Poll: Pod '%s' FOUND", self.pod_name)
            return None
        else:
            self.log.debug("Poll: Pod '%s' NOT found", self.pod_name)
            return 0

    @gen.coroutine
    def stop(self):
        self.client.delete_pod(self.pod_name)
