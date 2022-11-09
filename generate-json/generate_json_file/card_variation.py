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
    print("Generating card_variation.json from card.json...\n")

    card_array = []
    card_variation_array = []

    inPath = Path(__file__).parent / "../../json/card.json"
    outPath = Path(__file__).parent / "../../json/card_variation.json"

    with inPath.open(newline='') as infile:
        card_array = json.load(infile)

        for card in card_array:
            card_object = json.loads(json.dumps(card))

            has_different_artists = len(card_object['artists']) > 1
            artists_switched_mid_print = len([x for x in card_object['artists'] if " — " in x or " – " in x or " - " in x]) > 0
            rarities_switched_mid_print = len([x for x in card_object['rarities'] if " — " in x or " – " in x or " - " in x]) > 0

            for variation_index, variation in enumerate(card_object['variations']):
                card_variation = json.loads(json.dumps(card_object))

                variationSplit = re.split("— | – | - ", variation.strip())
                imageUrlData = [convert_image_data(x) for x in card_variation['image_urls']]

                foilings = variationSplit[0].strip().split(' ')
                cardIdFromVariation = variationSplit[1]
                setEdition = variationSplit[2]
                alternateArtType = None
                if len(variationSplit) >= 4:
                    alternateArtType = variationSplit[3]

                cardIdIndex = card_variation['ids'].index(cardIdFromVariation)

                set_id = card_variation['set_ids'][cardIdIndex]

                if has_different_artists:
                    if artists_switched_mid_print:
                        artist = card_variation['artists'][variation_index]

                        if len([x for x in card_object['artists'] if " — " in x or " – " in x or " - " in x]) > 0:
                            artist = re.split("— | – | - ", artist)[0]
                    else:
                        artist = card_variation['artists'][cardIdIndex]
                else:
                    artist = card_variation['artists'][0]

                if rarities_switched_mid_print:
                    rarity = card_variation['rarities'][variation_index]

                    if len([x for x in card_object['rarities'] if " — " in x or " – " in x or " - " in x]) > 0:
                            rarity = re.split("— | – | - ", rarity)[0]
                else:
                    rarity = card_variation['rarities'][0]

                valid_image_urls = [data for data in imageUrlData if data['card_id'] == cardIdFromVariation and data['set_edition'] == setEdition and data['alternate_art_type'] == alternateArtType]
                image_url = valid_image_urls[0]['image_url'] if len(valid_image_urls) > 0 else None

                card_variation['id'] = cardIdFromVariation
                card_variation['set_id'] = set_id
                card_variation['edition'] = setEdition
                card_variation['foilings'] = foilings
                card_variation['rarity'] = rarity
                card_variation['artist'] = artist
                card_variation['art_variation'] = alternateArtType
                card_variation['image_url'] = image_url

                del card_variation['ids']
                del card_variation['set_ids']
                del card_variation['rarities']
                del card_variation['types']
                del card_variation['artists']
                del card_variation['variations']
                del card_variation['image_urls']

                card_variation_array.append(card_variation)

    json_object = json.dumps(card_variation_array, indent=4)

    with outPath.open('w', newline='\n') as outfile:
        outfile.write(json_object)

    print("\nSuccessfully generated card_variation.json\n")