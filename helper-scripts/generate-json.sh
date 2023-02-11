#!/bin/bash

[ -d "helper-scripts" ] && cd helper-scripts

cd ./generate-json

if type pyenv >/dev/null 2>&1; then
    pyenv exec poetry run python main.py
else
    python main.py
fi
cd ..
