#!/bin/bash

[ -d "helper-scripts" ] && cd helper-scripts

./clean-csvs.sh || exit $?
echo ""
./validate-references.sh || exit $?
echo ""
./generate-artists.sh || exit $?
echo ""
./generate-unique-ids.sh || exit $?
echo ""
./generate-json.sh || exit $?
echo ""
./validate-json.sh || exit $?