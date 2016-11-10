# JupyterHub Kubernetes Spawner

Enables [JupyterHub](https://github.com/jupyterhub/jupyterhub) to spawn user servers inside Kubernetes.

## Install

```
python setup.py install

OR

pip install git+git://github.com/bjolivot/jupyterhub-kubernetes_spawner.git
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

### Volume management

If you want notebook files to be persisted you will need to mount volume in the spawned pod.
You can use one of these mode : nfs, glusterfs, persistent volume claim
 
 
Based on KubernetesSpawner.volume_mode, you will need to define different variables (look at k8s doc for help) :
 
####  `KubernetesSpawner.volume_mode == "nfs"`
 
 `KubernetesSpawner.nfs_server_ip`
 `KubernetesSpawner.nfs_server_share`
 
 
#### `KubernetesSpawner.volume_mode == "glusterfs"`
 `KubernetesSpawner.glusterfs_endpoint`
 `KubernetesSpawner.glusterfs_path`
 
#### `KubernetesSpawner.volume_mode == "persistent_volume_claim"`
`KubernetesSpawner.persistent_volume_claim_name` `KubernetesSpawner.persistent_volume_claim_path`

See example

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
c.KubernetesSpawner.volume_mode = "glusterfs"
c.KubernetesSpawner.glusterfs_endpoint = "glusterfs-cluster"
c.KubernetesSpawner.glusterfs_path = "jupyter-gluster"
```
