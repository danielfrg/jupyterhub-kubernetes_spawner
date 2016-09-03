FROM jupyterhub/jupyterhub

RUN apt-get update && apt-get install -y curl
RUN pip install jupyterhub-ldapauthenticator
RUN pip install git+git://github.com/danielfrg/jupyterhub-kubernetes_spawner.git

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py
COPY start.sh /srv/jupyterhub/start.sh
RUN chmod +x /srv/jupyterhub/start.sh

CMD ["/srv/jupyterhub/start.sh"]
