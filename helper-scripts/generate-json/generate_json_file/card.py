import csv
import json
import re
from pathlib import Path
from markdown_patch import unmark

def convert_to_array(field):
    return [x for x in field.split(", ") if x.strip() != ""]

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

def treat_string_as_boolean(field, default_value=True):
    return bool(treat_blank_string_as_boolean(field, default_value))

def treat_blank_string_as_boolean(field, default_value=True):
    if field == '':
        return default_value

    return field

def treat_blank_string_as_none(field):
    if field == '':
        return None

    return None

def generate_json_file():
    print("Filling out card.json from card.csv...")

    card_array = []

    csvPath = Path(__file__).parent / "../../../csvs/card.csv"
    jsonPath = Path(__file__).parent / "../../../json/card.json"

    with csvPath.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            card_object = {}

            rowId = 0

            ids = convert_to_array(row[rowId])
            rowId += 1

            set_ids = convert_to_array(row[rowId])
            rowId += 1

            card_object['name'] = row[rowId]
            rowId += 1

            card_object['pitch'] = row[rowId]
            rowId += 1

            card_object['cost'] = row[rowId]
            rowId += 1

            card_object['power'] = row[rowId]
            rowId += 1

            card_object['defense'] = row[rowId]
            rowId += 1

            card_object['health'] = row[rowId]
            rowId += 1

            card_object['intelligence'] = row[rowId]
            rowId += 1

            rarities = convert_to_array(row[rowId])
            rowId += 1

            card_object['types'] = convert_to_array(row[rowId])
            rowId += 1

            card_object['card_keywords'] = convert_to_array(row[rowId])
            rowId += 1

            card_object['abilities_and_effects'] = convert_to_array(row[rowId])
            rowId += 1

            card_object['ability_and_effect_keywords'] = convert_to_array(row[rowId])
            rowId += 1

            card_object['granted_keywords'] = convert_to_array(row[rowId])
            rowId += 1

            card_object['functional_text'] = row[rowId]
            rowId += 1

            card_object['functional_text_plain'] = unmark(card_object['functional_text'])

            card_object['flavor_text'] = row[rowId]
            rowId += 1

            card_object['flavor_text_plain'] = unmark(card_object['flavor_text'])

            card_object['type_text'] = row[rowId]
            rowId += 1

            artists = convert_to_array(row[rowId])
            rowId += 1

            card_object['played_horizontally'] = treat_string_as_boolean(row[rowId], default_value=False)
            rowId += 1

            card_object['blitz_legal'] = treat_string_as_boolean(row[rowId])
            rowId += 1

            card_object['cc_legal'] = treat_string_as_boolean(row[rowId])
            rowId += 1

            card_object['commoner_legal'] = treat_string_as_boolean(row[rowId])
            rowId += 1

            card_object['blitz_living_legend'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['cc_living_legend'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['blitz_banned'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['cc_banned'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['commoner_banned'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['upf_banned'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['blitz_suspended_start'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['blitz_suspended_end'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['cc_suspended_start'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['cc_suspended_end'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['commoner_suspended_start'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            card_object['commoner_suspended_end'] = treat_blank_string_as_none(row[rowId])
            rowId += 1

            variations = convert_to_array(row[rowId])
            rowId += 1

            image_urls = convert_to_array(row[rowId])
            rowId += 1

            # Clean up fields

            if card_object['played_horizontally'] == '':
                card_object['played_horizontally'] = False
            if card_object['blitz_legal'] == '':
                card_object['blitz_legal'] = True
            if card_object['cc_legal'] == '':
                card_object['cc_legal'] = True
            if card_object['commoner_legal'] == '':
                card_object['commoner_legal'] = True

            card_object['functional_text'] = card_object['functional_text'].replace("'", "''")
            card_object['functional_text_plain'] = card_object['functional_text_plain'].replace("'", "''")
            card_object['flavor_text'] = card_object['flavor_text'].replace("'", "''")
            card_object['flavor_text_plain'] = card_object['flavor_text_plain'].replace("'", "''")


            # Card Printings

            card_printing_array = []

            has_different_artists = len(artists) > 1
            artists_switched_mid_print = len([x for x in artists if " — " in x or " – " in x or " - " in x]) > 0
            rarities_switched_mid_print = len([x for x in rarities if " — " in x or " – " in x or " - " in x]) > 0

            for variation_index, variation in enumerate(variations):
                card_variation = {}

                variationSplit = re.split("— | – | - ", variation.strip())
                imageUrlData = [convert_image_data(x) for x in image_urls]

                foilings = variationSplit[0].strip().split(' ')
                cardIdFromVariation = variationSplit[1]
                setEdition = variationSplit[2]
                alternateArtType = None
                if len(variationSplit) >= 4:
                    alternateArtType = variationSplit[3]

                cardIdIndex = ids.index(cardIdFromVariation)

                set_id = set_ids[cardIdIndex]

                if has_different_artists:
                    if artists_switched_mid_print:
                        artist = artists[variation_index]

                        if len([x for x in artists if " — " in x or " – " in x or " - " in x]) > 0:
                            artist = re.split("— | – | - ", artist)[0]
                    else:
                        artist = artists[cardIdIndex]
                else:
                    artist = artists[0]

                if rarities_switched_mid_print:
                    rarity = rarities[variation_index]

                    if len([x for x in rarities if " — " in x or " – " in x or " - " in x]) > 0:
                            rarity = re.split("— | – | - ", rarity)[0]
                else:
                    rarity = rarities[0]

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

                card_printing_array.append(card_variation)

            card_object['printings'] = card_printing_array

            card_array.append(card_object)

    json_object = json.dumps(card_array, indent=4)

    with jsonPath.open('w', newline='\n') as outfile:
        outfile.write(json_object)

    print("Successfully generated card.csv\n")