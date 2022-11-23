#!/bin/bash

./generate-artists.sh
echo ""
./generate-json.sh
echo ""
./validate-json.sh
echo ""
./generate-htmls.sh