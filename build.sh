#!/bin/bash

GITHUB_REPO=$1
GITHUB_ORG=$2
GITHUB_TOKEN=$3



clone() {
  git clone https://${GITHUB_TOKEN}@github.com/${GITHUB_ORG}/${GITHUB_REPO}.git
}

build_doc() {
  cd ${GITHUB_REPO}
  /build/${GITHUB_REPO}/build.sh
}


clone()
build_doc()