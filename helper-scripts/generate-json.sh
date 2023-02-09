#!/bin/bash

[ -d "helper-scripts" ] && cd helper-scripts

cd ./generate-json
if type pyenv; then
    pyenv exec poetry run python main.py
else
    python main.py
fi
cd ..
