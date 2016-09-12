#!/bin/bash

if [ -z ${NOTEBOOK_DIR+x} ]; then
    echo "NOTEBOOK_DIR is unset";
else
    echo "NOTEBOOK_DIR is set to $NOTEBOOK_DIR";
    mkdir -p $NOTEBOOK_DIR
fi

sh /srv/singleuser/singleuser.sh
