#!/bin/bash

set -x

GITHUB_REPO=$1
GITHUB_ORG=$2
GITHUB_TOKEN=$3



clone() {
  echo "[+] Cloning repo ${GITHUB_REPO}"
  git clone https://${GITHUB_TOKEN}@github.com/${GITHUB_ORG}/${GITHUB_REPO}.git
}

build_doc() {
  echo "[+] Building doc for ${DOCKER_REPO}"
  cd ${GITHUB_REPO}
  /build/${GITHUB_REPO}/build.sh
}

publish_doc() {
  echo "[+] Publishing doc..."
  cd ${GITHUB_REPO}
  mkdocs gh-deploy
}

clone()
build_doc()
publish_doc()