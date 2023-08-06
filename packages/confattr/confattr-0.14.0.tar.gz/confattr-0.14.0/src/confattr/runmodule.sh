#!/usr/bin/env bash

if [ "$1" = '-i' ]; then
	ARGS=-i
	shift
else
	ARGS=
fi
../../venv/bin/python $ARGS -c "from confattr.${1%.py} import *"
