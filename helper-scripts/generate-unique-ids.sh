#!/bin/bash

[ -d "helper-scripts" ] && cd helper-scripts

cd ./generate-unique-ids

source ~/.nvm/nvm.sh

if command -v nvm &> /dev/null
then
    nvm use
fi

[ -d "node_packages" ] && npm i
npm run start
