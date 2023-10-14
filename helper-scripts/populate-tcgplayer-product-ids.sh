#!/bin/bash

[ -d "helper-scripts" ] && cd helper-scripts

cd ./populate-tcgplayer-product-ids

source ~/.nvm/nvm.sh

if command -v nvm &> /dev/null
then
    nvm use
fi

[ -d "node_packages" ] && npm i
npm run start "$@"