#!/bin/bash

[ -d "helper-scripts" ] && cd helper-scripts

cd ./clean-csvs

if type pyenv >/dev/null 2>&1; then
    pyenv exec poetry run python main.py || exit $?
else
    python main.py || exit $?
fi
cd ..
