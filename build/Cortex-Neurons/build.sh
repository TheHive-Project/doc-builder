#!/bin/bash

set -e

TYPE=$1

die() {
  echo $* >&2
  exit 2
}

build_doc() {
  echo "[+] Building doc for ${TYPE}"
  
  /usr/local/bin/${TYPE}/generate.py
  cp -v CHANGELOG.md docs/.
  cp -v code_of_conduct.md docs/.
  cp -rv images docs/
  cp -rv README.md docs/
}

[[ -z "$TYPE" ]] && die "No type setting given (./build.sh <TYPE>) "

build_doc
# while [[ $# -gt 0 ]]; do
#   build_doc
# done






