FROM jupyterhub/jupyterhub

RUN apt-get update && apt-get install -y curl
RUN pip install jupyterhub-ldapauthenticator oauthenticator

USER root
COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

CMD ["/startup.sh"]
