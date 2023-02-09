#!/bin/bash

if type pyenv > /dev/null 2>&1; then
    CMD="pyenv exec poetry run generate-schema-doc"
else
    CMD="generate-schema-doc"
fi

$CMD --config-file conf.yaml ../../json-schema ../../web/json-schemas
