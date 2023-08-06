#!/bin/bash

set -e

/opt/sbin/create-user.sh

for kernel_file in $(find ${WORKSPACE} -name kernel.json)
do
  kernel_path=$(dirname $kernel_file)
	ln -s $kernel_path /usr/local/share/jupyter/kernels
done

exec su $USER -s /bin/bash -c "jupyter lab --debug --notebook-dir=${WORKSPACE}"

# --keyfile=${LAB_CA}/jupyter-key.pem --certfile=${LAB_CA}/jupyter-cert.pem

