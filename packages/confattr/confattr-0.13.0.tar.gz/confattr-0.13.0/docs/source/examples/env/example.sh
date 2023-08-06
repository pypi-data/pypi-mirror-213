#!/usr/bin/env bash

# enable strict mode
set -euo pipefail

# change to the directory where this file is located because tox runs it from somewhere else
cd "$(dirname "${BASH_SOURCE[0]}")"

python="$1"
example-app() { "$python" example.py; }

# ------- start -------
EXAMPLE_APP_UI_GREETING='hello environment' example-app
