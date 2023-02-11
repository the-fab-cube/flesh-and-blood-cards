#!/bin/bash

[ -d "helper-scripts" ] && cd helper-scripts

cd ./generate-unique-ids

[ -d "node_packages" ] && npm i
npm run start
