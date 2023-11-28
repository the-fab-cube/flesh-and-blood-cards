from os import makedirs
from os.path import exists

import generate_json_file.ability
import generate_json_file.art_variation
import generate_json_file.artist
import generate_json_file.card
import generate_json_file.card_face_association
import generate_json_file.card_flattened
import generate_json_file.card_non_english
import generate_json_file.card_reference
import generate_json_file.edition
import generate_json_file.foiling
import generate_json_file.icon
import generate_json_file.keyword
import generate_json_file.legality
import generate_json_file.rarity
import generate_json_file.set
import generate_json_file.type

json_dir_path = "../../json/"
english_json_dir_path = json_dir_path + "english/"

print("Generating JSON data...\n")

if not exists(json_dir_path):
    print(json_dir_path + " does not exist, creating it")
    makedirs(json_dir_path)

if not exists(english_json_dir_path):
    print(english_json_dir_path + " does not exist, creating it")
    makedirs(english_json_dir_path)

# English JSON files #
generate_json_file.ability.generate_json_file("english")
generate_json_file.artist.generate_json_file("english")
generate_json_file.set.generate_json_file("english")
generate_json_file.card_face_association.generate_json_file("english")
generate_json_file.card_reference.generate_json_file()

generate_json_file.legality.generate_json_file("banned-blitz")
generate_json_file.legality.generate_json_file("banned-cc")
generate_json_file.legality.generate_json_file("banned-commoner")
generate_json_file.legality.generate_json_file("banned-upf")
generate_json_file.legality.generate_json_file("living-legend-blitz")
generate_json_file.legality.generate_json_file("living-legend-cc")
generate_json_file.legality.generate_json_file("suspended-blitz")
generate_json_file.legality.generate_json_file("suspended-cc")
generate_json_file.legality.generate_json_file("suspended-commoner")
generate_json_file.legality.generate_json_file("restricted-ll")

generate_json_file.art_variation.generate_json_file()
generate_json_file.card.generate_json_file()
generate_json_file.card_flattened.generate_json_file("english")
generate_json_file.edition.generate_json_file()
generate_json_file.foiling.generate_json_file()
generate_json_file.icon.generate_json_file()
generate_json_file.keyword.generate_json_file("english")
generate_json_file.rarity.generate_json_file()
generate_json_file.type.generate_json_file("english")

# Non-English JSON files #
generate_json_file.artist.generate_json_file("french")
generate_json_file.artist.generate_json_file("german")
generate_json_file.artist.generate_json_file("italian")
generate_json_file.artist.generate_json_file("spanish")

generate_json_file.ability.generate_json_file("french")
generate_json_file.ability.generate_json_file("german")
generate_json_file.ability.generate_json_file("italian")
generate_json_file.ability.generate_json_file("spanish")

generate_json_file.keyword.generate_json_file("french")
generate_json_file.keyword.generate_json_file("german")
generate_json_file.keyword.generate_json_file("italian")
generate_json_file.keyword.generate_json_file("spanish")

generate_json_file.set.generate_json_file("french")
generate_json_file.set.generate_json_file("german")
generate_json_file.set.generate_json_file("italian")
generate_json_file.set.generate_json_file("spanish")

generate_json_file.type.generate_json_file("french")
generate_json_file.type.generate_json_file("german")
generate_json_file.type.generate_json_file("italian")
generate_json_file.type.generate_json_file("spanish")

# These rely on the other Non-English JSON files being generated first
generate_json_file.card_non_english.generate_json_file("french")
generate_json_file.card_non_english.generate_json_file("german")
generate_json_file.card_non_english.generate_json_file("italian")
generate_json_file.card_non_english.generate_json_file("spanish")

generate_json_file.card_flattened.generate_json_file("french")
generate_json_file.card_flattened.generate_json_file("german")
generate_json_file.card_flattened.generate_json_file("italian")
generate_json_file.card_flattened.generate_json_file("spanish")

print("Finished generating JSON data")