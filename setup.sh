#!/usr/bin/env bash

SCRIPT_PATH=$(dirname "${BASH_SOURCE[0]}")
VENV_PATH="${SCRIPT_PATH}/venv"
VENV_PATH_FULL="$(readlink -fs "${VENV_PATH}")"
REINSTALL=false

function usage() {
  echo "Usage: $(basename "${BASH_SOURCE[0]}") [options]"
  echo
  echo "Options:"
  echo "  -f | --force      force-remove old venv files"
}

while test $# -gt 0 ; do
  arg="$1"
  shift

  case "$arg" in
    -f | --force)
      REINSTALL=true
      ;;
    *)
      usage
      exit 1
      ;;
  esac
done

if test "${REINSTALL}" = "true" -a -d "${VENV_PATH}" ; then
  echo "Removing virtual environment: ${VENV_PATH_FULL}"
  rm -rf "${VENV_PATH}"
fi

if test ! -d "${VENV_PATH}" ; then
  echo "Creating virtual environment: ${VENV_PATH_FULL}"
  python -mvenv "${VENV_PATH}"
fi

echo "Your virtual environment is installed at"
echo
echo "    ${VENV_PATH_FULL}"
echo
echo "Activate your virtual environment with this command:"
echo
echo "    source \"${VENV_PATH}/bin/activate\""
echo
echo "Deactivate your virtual environment with this command:"
echo
echo "    deactivate"