from os import makedirs
from os.path import exists

import generate_json_file.artist
import generate_json_file.card
import generate_json_file.card_flattened
import generate_json_file.edition
import generate_json_file.foiling
import generate_json_file.icon
import generate_json_file.keyword
import generate_json_file.rarity
import generate_json_file.set
import generate_json_file.type

json_dir_path = "../../json/"
english_json_dir_path = json_dir_path + "english/"

def generate_json_file_data():
    print("Generating JSON data...\n")

    if not exists(json_dir_path):
        print(json_dir_path + " does not exist, creating it")
        makedirs(json_dir_path)

    if not exists(english_json_dir_path):
        print(english_json_dir_path + " does not exist, creating it")
        makedirs(english_json_dir_path)

    generate_json_file.artist.generate_json_file()
    generate_json_file.card.generate_json_file()
    generate_json_file.card_flattened.generate_json_file()
    generate_json_file.edition.generate_json_file()
    generate_json_file.foiling.generate_json_file()
    generate_json_file.icon.generate_json_file()
    generate_json_file.keyword.generate_json_file()
    generate_json_file.rarity.generate_json_file()
    generate_json_file.set.generate_json_file()
    generate_json_file.type.generate_json_file()

    print("Finished generating JSON data")