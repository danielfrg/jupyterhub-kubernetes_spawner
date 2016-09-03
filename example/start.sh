#!/bin/bash

while true; do
    echo "Checking for configurable-http-proxy"
    response=$(curl --write-out %{http_code} --silent --output /dev/null http://127.0.0.1:8001)
    echo "configurable-http-proxy status: $response"
    if [ ${response} != "000" ]; then
        break;
    else
        sleep 2
    fi
done

# pip install git+git://github.com/danielfrg/jupyterhub-kubernetes_spawner.git
jupyterhub --ip 0.0.0.0 --no-ssl --log-level DEBUG
