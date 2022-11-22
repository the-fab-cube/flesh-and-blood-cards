#!/bin/bash

./node_modules/pajv/index.js validate -s ../json-schema/artist-schema.json -d ../json/artist.json
./node_modules/pajv/index.js validate -s ../json-schema/card_variation-schema.json -d ../json/card_variation.json