#!/bin/bash

[ -d "helper-scripts" ] && cd helper-scripts

cd ./generate-unique-ids
npm run start
cd ..