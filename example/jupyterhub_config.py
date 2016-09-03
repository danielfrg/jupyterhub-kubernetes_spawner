
c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator'
c.LDAPAuthenticator.bind_dn_template = 'cn={username},cn=jupyterhub,dc=example,dc=org'
c.LDAPAuthenticator.server_address = '{ LDAP_POD_ID }'
c.LDAPAuthenticator.use_ssl = False

c.JupyterHub.spawner_class = 'kubernetes_spawner.KubernetesSpawner'
c.KubernetesSpawner.host = '{ KUBE_HOST }'
c.KubernetesSpawner.username = '{ KUBE_USER }'
c.KubernetesSpawner.password = '{ KUBE_PASS }'
c.KubernetesSpawner.verify_ssl = False
c.KubernetesSpawner.hub_ip_from_service = "jupyterhub"
