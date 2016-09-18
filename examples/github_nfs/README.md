# JupyterHub on Kubernetes with GitHub OAuth and NFS

## GitHub

Using the [Jupyter Hub oauthenticator](https://github.com/jupyterhub/oauthenticator).

Create a new application on the [GitHub application settings](https://github.com/settings/developers/):

1. In the `Authorization callback URL` do: `http[s]://[your-host]/hub/oauth_callback`
2. Now you should have `Client ID` and `Client Secret` and need to encode them as base64

```
$ echo -n 'CLIENT_ID' | base64
ENCODED_BASE64_CLIENT_ID

$ echo -n 'CLIENT_SECRET' | base64
ENCODED_BASE64_CLIENT_SECRET
```

Edit the `secrets.yml` file and add the base64 encoded values.

```
$ kubectl create -f secrets.yml
```

## NFS

```
$ kubectl create -f nfs.yml
```

1. Get service `Cluster-IP` for the `jupyterhub-nfs` service: `kubectl get service | grep jupyterhub-nfs`
2. Edit the `nfs2.yml` file and replace `{{ X.X.X.X }}` with the ip of the service found in (1)

```
$ kubectl create -f nfs2.yml
```

Two services are now running:

1. `jupyterhub-nfs`: NFS server
2. `jupyterhub-nfs-web`: An optional simple NGINX (`autoindex: on;`) to browse the files

One Persistent Volume Claim (`jupyterhub-volume`) is ready for the JupyterHub single user pods.

## JupyterHub

Edit `hub.yml` and add the oauth callback URL at `{{ OAUTH_CALLBACK_URL }}`.

```
$ kubectl create -f hub.yml
```

Two services are now running:

1. `jupyterhub`: Main JupyterHub UI. Login as any LDAP user as defined in the ConfigMap
2. `jupyterhub-api`: JupyterHub API - not really useful for users
