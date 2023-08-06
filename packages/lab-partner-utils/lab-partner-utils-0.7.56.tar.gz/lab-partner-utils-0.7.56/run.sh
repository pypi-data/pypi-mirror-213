#!/bin/bash

set -e

cmd=$1

version() {
  grep -Ei "^version" pyproject.toml | grep -Eio "([0-9]+\.[0-9]+\.[0-9]+)"
}

docker run -it --rm \
  -e WORKSPACE=${WORKSPACE} \
  -v ${WORKSPACE}:${WORKSPACE} \
  enclarify/lab-partner-utils:$(version) ${cmd}
