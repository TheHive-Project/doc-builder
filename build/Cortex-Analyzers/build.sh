#!/bin/bash

set -x

GITHUB_REPO=$1
GITHUB_ORG=$2
GITHUB_TOKEN=$3

MYPATH=`realpath $0`
MYDIR=`dirname ${path}`

build_doc() {
  echo "[+] Building doc for ${GITHUB_REPO}"
  
  python3 generate.py
  cp -v CHANGELOG.md dozcs/.
  cp -v code_of_conduct.md docs/.
  cp -rv images docs/
  cp -rv README.md docs/
}

publish_doc(){
  echo "[+] Publishing doc for ${GITHUB_REPO}"
  mkdocs gh-deploy
}


clone
cd ${GITHUB_REPO}
build_doc
publish_doc