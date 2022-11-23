#!/bin/bash

./node_modules/pajv/index.js validate -s ../json-schema/artist-schema.json -d ../json/artist.json
./node_modules/pajv/index.js validate -s ../json-schema/card-schema.json -d ../json/card.json
./node_modules/pajv/index.js validate -s ../json-schema/card-flattened-schema.json -d ../json/card-flattened.json
./node_modules/pajv/index.js validate -s ../json-schema/edition-schema.json -d ../json/edition.json
./node_modules/pajv/index.js validate -s ../json-schema/foiling-schema.json -d ../json/foiling.json
./node_modules/pajv/index.js validate -s ../json-schema/icon-schema.json -d ../json/icon.json
./node_modules/pajv/index.js validate -s ../json-schema/keyword-schema.json -d ../json/keyword.json
./node_modules/pajv/index.js validate -s ../json-schema/rarity-schema.json -d ../json/rarity.json
./node_modules/pajv/index.js validate -s ../json-schema/set-schema.json -d ../json/set.json
./node_modules/pajv/index.js validate -s ../json-schema/type-schema.json -d ../json/type.json