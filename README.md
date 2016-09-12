# JupyterHub Kubernetes Spawner

Enables [JupyterHub](https://github.com/jupyterhub/jupyterhub) to spawn user servers inside Kubernetes.

## Install

```
python setup.py install

OR

pip install git+git://github.com/danielfrg/jupyterhub-kubernetes_spawner.git
```

## Usage

Tell JupyterHub to use `KubernetesSpawner` by adding the following line to your `jupyterhub_config.py`:

```
c.JupyterHub.spawner_class = 'kubernetes_spawner.KubernetesSpawner'
```

### Configuration

By default the `KubernetesSpawner` will use a Kubernetes Service Account to communicate
with Kubernetes so in theory it could work without a any of configuration, in practice
you might need to change some of the settings.

#### `KubernetesSpawner.host`

`default=https://kubernetes`

Host of the Kuberentes API. The default `kuberentes` host is found in the Kubernetes DNS.

#### `KubernetesSpawner.username` and `KubernetesSpawner.password`

The default auth for the Kubernetes API is the Kuberentes Service Account mounted
in the pod but is possible to overwrite it with this settings.
This is more useful in development and not recommended for the deployment.

#### `KubernetesSpawner.verify_ssl`

`default=True`

Whether to verify SSL connection to the Kubernetes API

#### `KubernetesSpawner.container_image`
`default=jupyterhub/singleuser`

Image to use as for the single user container notebooks.

#### `KubernetesSpawner.container_port`
`default=8888`

Notebook port exposed by the single user container image

####  `KubernetesSpawner.persistent_volume_claim_name` and `KubernetesSpawner.persistent_volume_claim_path`

If you want notebook files to be persisted set these values to a
Kubernetes Persistent Volume Claim and a mount path on the
container.

This will probably require to change `c.Spawner.notebook_dir`
to a path inside `KubernetesSpawner.persistent_volume_claim_path`.
See example.

#### `KubernetesSpawner.hub_ip_from_service`
`default=jupyterhub`

The single user containers need to find the IP of the JupyterHub.
You can set this setting to find a Kubernetes Service name
to tell the single user notebooks the correct IP.

### Example

There is a complete example in `examples/ldap_nfs` for using LDAP to authenticate users
and spawn containers inside kubernetes, the user notebooks are backed by an NFS server.

The example walks trought the deployment of every piece.

The settings on that example look something like this:

```python
c.JupyterHub.confirm_no_ssl = True
c.JupyterHub.db_url = 'sqlite:////tmp/jupyterhub.sqlite'
c.JupyterHub.cookie_secret_file = '/tmp/jupyterhub_cookie_secret'

c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator'
c.LDAPAuthenticator.bind_dn_template = 'cn={username},cn=jupyterhub,dc=example,dc=org'
c.LDAPAuthenticator.server_address = '{{ LDAP_SERVICE }}'
c.LDAPAuthenticator.use_ssl = False

c.JupyterHub.spawner_class = 'kubernetes_spawner.KubernetesSpawner'
c.KubernetesSpawner.verify_ssl = False
c.KubernetesSpawner.hub_ip_from_service = 'jupyterhub'
c.KubernetesSpawner.container_image = 'danielfrg/jupyterhub-kube-ldap-nfs-singleuser:0.1'
c.Spawner.notebook_dir = '/mnt/notebooks/%U'
c.KubernetesSpawner.persistent_volume_claim_name = 'jupyterhub-volume'
c.KubernetesSpawner.persistent_volume_claim_path = '/mnt'
```
