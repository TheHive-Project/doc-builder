#!/bin/bash

set -x

GITHUB_REPO=$1
GITHUB_ORG=$2
GITHUB_TOKEN=$3

MYPATH=`realpath $0`
MYDIR=`dirname ${path}`

clone() {
  echo "[+] Cloning repo ${GITHUB_REPO}"
  git clone https://${GITHUB_TOKEN}@github.com/${GITHUB_ORG}/${GITHUB_REPO}.git
}

build_doc() {
  echo "[+] Building  and publishing the doc for ${GITHUB_REPO}"
  cp build/${GITHUB_REPO}/* ${GITHUB_REPO}/
  cd ${GITHUB_REPO}
  /bin/bash build.sh
}

clone
build_doc