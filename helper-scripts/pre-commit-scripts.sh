#!/bin/bash

[ -d "helper-scripts" ] && cd helper-scripts

./generate-artists.sh || exit $?
echo ""
./generate-unique-ids.sh || exit $?
echo ""
./generate-json.sh || exit $?
echo ""
./validate-json.sh || exit $?
echo ""
./generate-htmls.sh || exit $?