#!/usr/bin/env bash

BUILD_MODE=dev
VERSION="$(date "+%Y.%m.%d.%H.%M.%S.%s")"

function usage() {
  echo "Usage: $(basename "${BASH_SOURCE[0]}") [options]"
  echo
  echo "Options:"
  echo "  -r | --release    build library in release mode"
  echo "                    default is dev"
}

while test $# -gt 0 ; do
  arg="$1"
  shift

  case "$arg" in
    -r | --release)
      BUILD_MODE=release
      ;;
    *)
      usage
      exit 1
      ;;
  esac
done

pip install build hatch

hatch version "${VERSION}"
if test "$BUILD_MODE" != "release" ; then
  hatch version "$BUILD_MODE"
fi
python -m build
