import json
import getopt
import re
import requests
from os import makedirs
from os.path import exists
from pathlib import Path
import sys

images_dir_path = "images/"
set_id_to_download = None

def download_images_from_language_data(language):
    # Download the images
    path = Path(__file__).parent / f"../../json/{language}/card.json"
    with path.open(newline='') as jsonfile:
        card_array = json.load(jsonfile)

        for card in card_array:
            for printing in card['printings']:
                image_url = printing['image_url']
                set_id = printing['set_id']

                if image_url is not None and (set_id_to_download == None or set_id == set_id_to_download):
                        download_image_from_url(image_url)


def download_image_from_url(image_url: str):
    cleaned_up_image_url = image_url.replace("https://storage.googleapis.com/fabmaster/media/images/", "")
    cleaned_up_image_url = cleaned_up_image_url.replace("https://storage.googleapis.com/fabmaster/cardfaces/", "")
    cleaned_up_image_url = cleaned_up_image_url.replace("https://dhhim4ltzu1pj.cloudfront.net/media/images/", "")
    cleaned_up_image_url = cleaned_up_image_url.replace("https://d2wlb52bya4y8z.cloudfront.net/media/cards/", "")

    file_name = "images/" + cleaned_up_image_url
    if exists(file_name):
        print(file_name + " already exists, skipping")
        return

    file_dir = "/".join(file_name.split("/")[:-1])
    if not exists(file_dir):
        print(file_dir + " does not exist, creating it")
        makedirs(file_dir)

    print("Downloading " + image_url + " to " + file_name)
    img_data = requests.get(image_url).content
    with open(file_name, 'wb') as handler:
        handler.write(img_data)

# Parse command line flags
try:
    opts, args = getopt.getopt(sys.argv[1:], "hs:")
except getopt.GetoptError:
    print('main.py -s <set-id>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print ('main.py -s <set-id>')
        sys.exit()
    elif opt in ("-s", "--set-id"):
        set_id_to_download = arg
        print("Downloading only", set_id_to_download, "images")

if not exists(images_dir_path):
    print(images_dir_path + " does not exist, creating it")
    makedirs(images_dir_path)


download_images_from_language_data("english")
download_images_from_language_data("french")
download_images_from_language_data("german")
download_images_from_language_data("italian")
download_images_from_language_data("spanish")