import csv
import getopt
import re
import requests
from os import makedirs
from os.path import exists
from pathlib import Path
import sys

images_dir_path = "images/"
set_id_to_download = None

def download_image_from_url(image_url: str):
    cleaned_up_image_url = image_url.replace("https://storage.googleapis.com/fabmaster/media/images/", "")
    cleaned_up_image_url = cleaned_up_image_url.replace("https://storage.googleapis.com/fabmaster/cardfaces/", "")

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

path = Path(__file__).parent / "../../csvs/card.csv"
with path.open(newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
    next(reader)

    for row in reader:
        # indices: 0 is url, 1 is cardid, 2 is edition, 3 is variations
        image_urls_split = [re.split("— | – | - ", url.strip()) for url in row[36].split(',')]
        for image_url_data in image_urls_split:
            if len(image_url_data) >= 3 and (set_id_to_download == None or image_url_data[1].find(set_id_to_download) >= 0):
                download_image_from_url(image_url_data[0])

