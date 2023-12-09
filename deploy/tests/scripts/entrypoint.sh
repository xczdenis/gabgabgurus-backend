#!/bin/sh
set -e

./scripts/wait-dependencies.sh

. ./.venv/bin/activate

exec "$@"
