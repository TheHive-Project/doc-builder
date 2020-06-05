#!/bin/bash

set -e

help() {
  cat <<-_EOF_
  Building documentation files
  Udate: $0 [OPTION...]
  Arguments:
    -t, --type          Build type 
    -h, --help          This message
_EOF_
  exit 1
}

die() {
  echo $* >&2
  exit 2
}

while [[ $# -gt 0 ]]; do
  case $1 in
    -t|--type)        PLUGIN_TYPE=$2;     shift 2;;
    *)                 help;                shift 1;;
  esac
done

[[ -z "$PLUGIN_TYPE" ]] && die "No type setting given (setting \"--type\")"

/usr/local/bin/${PLUGIN_TYPE}/build.sh ${PLUGIN_TYPE}