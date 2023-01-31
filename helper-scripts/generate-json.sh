#!/bin/bash

cd ./generate-json
pyenv exec poetry run python main.py
cd ..