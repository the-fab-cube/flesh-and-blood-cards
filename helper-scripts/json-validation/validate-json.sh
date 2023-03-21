#!/bin/bash

[ -x ./node_modules/pajv/index.js ] || npm i

function validate_json {
    ./node_modules/pajv/index.js validate -s $1 -d $2  || exit $?
}

CMD="./node_modules/pajv/index.js validate -s"

validate_json ../../json-schema/ability-schema.json ../../json/english/ability.json
validate_json ../../json-schema/artist-schema.json ../../json/english/artist.json
validate_json ../../json-schema/card-schema.json ../../json/english/card.json
validate_json ../../json-schema/card-flattened-schema.json ../../json/english/card-flattened.json
validate_json ../../json-schema/card-face-association-schema.json ../../json/english/card-face-association.json
validate_json ../../json-schema/card-reference-schema.json ../../json/english/card-reference.json
validate_json ../../json-schema/edition-schema.json ../../json/english/edition.json
validate_json ../../json-schema/foiling-schema.json ../../json/english/foiling.json
validate_json ../../json-schema/icon-schema.json ../../json/english/icon.json
validate_json ../../json-schema/keyword-schema.json ../../json/english/keyword.json
validate_json ../../json-schema/legality-schema.json ../../json/english/banned-blitz.json
validate_json ../../json-schema/legality-schema.json ../../json/english/banned-cc.json
validate_json ../../json-schema/legality-schema.json ../../json/english/banned-commoner.json
validate_json ../../json-schema/legality-schema.json ../../json/english/banned-upf.json
validate_json ../../json-schema/legality-schema.json ../../json/english/living-legend-blitz.json
validate_json ../../json-schema/legality-schema.json ../../json/english/living-legend-cc.json
validate_json ../../json-schema/legality-schema.json ../../json/english/suspended-blitz.json
validate_json ../../json-schema/legality-schema.json ../../json/english/suspended-cc.json
validate_json ../../json-schema/legality-schema.json ../../json/english/suspended-commoner.json
validate_json ../../json-schema/rarity-schema.json ../../json/english/rarity.json
validate_json ../../json-schema/set-schema.json ../../json/english/set.json
validate_json ../../json-schema/type-schema.json ../../json/english/type.json

validate_json ../../json-schema/ability-schema.json ../../json/french/ability.json
validate_json ../../json-schema/artist-schema.json ../../json/french/artist.json
validate_json ../../json-schema/card-schema.json ../../json/french/card.json
validate_json ../../json-schema/card-flattened-schema.json ../../json/french/card-flattened.json
validate_json ../../json-schema/keyword-schema.json ../../json/french/keyword.json
validate_json ../../json-schema/set-schema.json ../../json/french/set.json
validate_json ../../json-schema/type-schema.json ../../json/french/type.json

validate_json ../../json-schema/ability-schema.json ../../json/german/ability.json
validate_json ../../json-schema/artist-schema.json ../../json/german/artist.json
validate_json ../../json-schema/card-schema.json ../../json/german/card.json
validate_json ../../json-schema/card-flattened-schema.json ../../json/german/card-flattened.json
validate_json ../../json-schema/keyword-schema.json ../../json/german/keyword.json
validate_json ../../json-schema/set-schema.json ../../json/german/set.json
validate_json ../../json-schema/type-schema.json ../../json/german/type.json

validate_json ../../json-schema/ability-schema.json ../../json/italian/ability.json
validate_json ../../json-schema/artist-schema.json ../../json/italian/artist.json
validate_json ../../json-schema/card-schema.json ../../json/italian/card.json
validate_json ../../json-schema/card-flattened-schema.json ../../json/italian/card-flattened.json
validate_json ../../json-schema/keyword-schema.json ../../json/italian/keyword.json
validate_json ../../json-schema/set-schema.json ../../json/italian/set.json
validate_json ../../json-schema/type-schema.json ../../json/italian/type.json

validate_json ../../json-schema/ability-schema.json ../../json/spanish/ability.json
validate_json ../../json-schema/artist-schema.json ../../json/spanish/artist.json
validate_json ../../json-schema/card-schema.json ../../json/spanish/card.json
validate_json ../../json-schema/card-flattened-schema.json ../../json/spanish/card-flattened.json
validate_json ../../json-schema/keyword-schema.json ../../json/spanish/keyword.json
validate_json ../../json-schema/set-schema.json ../../json/spanish/set.json
validate_json ../../json-schema/type-schema.json ../../json/spanish/type.json
