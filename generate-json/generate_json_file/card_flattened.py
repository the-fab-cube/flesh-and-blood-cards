import json
from pathlib import Path
import re

def convert_image_data(image_url):
    image_url_split = re.split("— | – | - ", image_url.strip())

    image_url_data = {}
    image_url_data['image_url'] = image_url_split[0]
    image_url_data['card_id'] = image_url_split[1]
    image_url_data['set_edition'] = image_url_split[2]
    image_url_data['alternate_art_type'] = None
    if len(image_url_split) >= 4:
        image_url_data['alternate_art_type'] = image_url_split[3]

    return image_url_data

def generate_json_file():
    print("Generating card-flattened.json from card.json...")

    card_array = []
    card_variation_array = []

    inPath = Path(__file__).parent / "../../json/card.json"
    outPath = Path(__file__).parent / "../../json/card-flattened.json"

    with inPath.open(newline='') as infile:
        card_array = json.load(infile)

        for card in card_array:
            card_object = json.loads(json.dumps(card))

            for _, printing in enumerate(card_object['printings']):
                card_variation = json.loads(json.dumps(card_object))

                card_variation['id'] = printing['id']
                card_variation['set_id'] = printing['set_id']
                card_variation['edition'] = printing['edition']
                card_variation['foilings'] = printing['foilings']
                card_variation['rarity'] = printing['rarity']
                card_variation['artist'] = printing['artist']
                card_variation['art_variation'] = printing['art_variation']
                card_variation['image_url'] = printing['image_url']

                del card_variation['printings']

                card_variation_array.append(card_variation)

    json_object = json.dumps(card_variation_array, indent=4)

    with outPath.open('w', newline='\n') as outfile:
        outfile.write(json_object)

    print("Successfully generated card-flattened.json\n")