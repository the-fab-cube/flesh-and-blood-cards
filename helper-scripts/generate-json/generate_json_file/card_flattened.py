import json
from pathlib import Path

def generate_json_file(language):
    print(f"Generating {language} card-flattened.json from card.json...")

    card_array = []
    card_printing_array = []

    inPath = Path(__file__).parent / f"../../../json/{language}/card.json"
    outPath = Path(__file__).parent / f"../../../json/{language}/card-flattened.json"

    with inPath.open(newline='') as infile:
        card_array = json.load(infile)

        for card in card_array:
            card_object = json.loads(json.dumps(card))

            for _, printing in enumerate(card_object['printings']):
                card_printing = json.loads(json.dumps(card_object))

                card_printing['printing_unique_id'] = printing['unique_id']
                card_printing['set_printing_unique_id'] = printing['set_printing_unique_id']
                card_printing['id'] = printing['id']
                card_printing['set_id'] = printing['set_id']
                card_printing['edition'] = printing['edition']
                card_printing['foiling'] = printing['foiling']
                card_printing['rarity'] = printing['rarity']
                card_printing['artist'] = printing['artist']
                card_printing['art_variation'] = printing['art_variation']
                card_printing['flavor_text'] = printing['flavor_text']
                card_printing['flavor_text_plain'] = printing['flavor_text_plain']
                card_printing['image_url'] = printing['image_url']
                if 'tcgplayer_product_id' in printing:
                    card_printing['tcgplayer_product_id'] = printing['tcgplayer_product_id']
                if 'tcgplayer_url' in printing:
                    card_printing['tcgplayer_url'] = printing['tcgplayer_url']
                if 'double_sided_card_info' in printing:
                    card_printing['double_sided_card_info'] = printing['double_sided_card_info']

                del card_printing['printings']

                card_printing_array.append(card_printing)

    json_object = json.dumps(card_printing_array, indent=4, ensure_ascii=False)

    with outPath.open('w', newline='\n', encoding='utf8') as outfile:
        outfile.write(json_object)

    print(f"Successfully generated {language} card-flattened.json\n")