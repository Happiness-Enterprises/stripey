#!/usr/bin/env bash

PATH="/venv/bin:$PATH"
PIP_REQUIREMENTS_ENTRYPOINT=/entrypoint.requirements.txt
GUNICORN_RUN_PORT=8000
GUNICORN_LOG_LEVEL=${GUNICORN_LOG_LEVEL:-info}
EXTRA_MIGRATION_ARGS=()

# Defaults for async comms.
export TELAPORT__CHANNEL__CHECKOUT_CREATE="${TELAPORT__CHANNEL__CHECKOUT_CREATE:-telaport_checkout_create}"
export BACKEND_URL="${BACKEND_URL:-http://localhost:8000/}"

# e.g. http://localhost:8000/telaport/api/
API_ENDPOINT="$(echo "${BACKEND_URL}" | sed 's,/$,,g;')/telaport/api/"

if test "${DJANGO_MIGRATE_SKIP_CHECKS}" = "true" ; then
  EXTRA_MIGRATION_ARGS+=("--skip-checks")
fi

if test -f "${PIP_REQUIREMENTS_ENTRYPOINT}" ; then
  pip install -r "${PIP_REQUIREMENTS_ENTRYPOINT}"
fi

set -x

# graphql_auth keeps placing migrations outside of django; therefore, run makemigrations here
python manage.py makemigrations graphql_auth --noinput "${EXTRA_MIGRATION_ARGS[@]}"
python manage.py migrate graphql_auth --noinput "${EXTRA_MIGRATION_ARGS[@]}"

# Django setup
python manage.py migrate --noinput "${EXTRA_MIGRATION_ARGS[@]}"
python manage.py collectstatic --noinput
# python manage.py compilemessages -v 0

set -x

# Start gunicorn, which will be available for nginx to reverse proxy.
gunicorn backend.wsgi:application \
  --bind "0.0.0.0:${GUNICORN_RUN_PORT}" \
  --daemon \
  --access-logfile '-' \
  --error-logfile '-' \
  --capture-output \
  --enable-stdio-inheritance \
  --reload \
  --log-level ${GUNICORN_LOG_LEVEL}

exec "$@"
