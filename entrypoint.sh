#!/bin/bash

set -x

clone() {
  echo "[+] Cloning repo ${GITHUB_REPO}"
  git clone https://${GITHUB_TOKEN}@github.com/${GITHUB_ORG}/${GITHUB_REPO}.git
  cp build/${GITHUB_REPO}/* ${GITHUB_REPO}/
}

clone
cd ${GITHUB_REPO}
/bin/bash build.sh ${GITHUB_ORG} ${GITHUB_REPO} ${GITHUB_TOKEN}