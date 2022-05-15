import csv
import re
import requests
from os import makedirs
from os.path import exists
from pathlib import Path

images_dir_path = "images/"

def download_image_from_url(image_url: str):
    cleaned_up_image_url = image_url.replace("https://storage.googleapis.com/fabmaster/media/images/", "")
    cleaned_up_image_url = cleaned_up_image_url.replace("https://storage.googleapis.com/fabmaster/cardfaces/2021-MON/", "")
    cleaned_up_image_url = cleaned_up_image_url.replace("https://storage.googleapis.com/fabmaster/cardfaces/2020-CRU/", "")
    cleaned_up_image_url = cleaned_up_image_url.replace("https://storage.googleapis.com/fabmaster/cardfaces/2021-ELE/", "")
    cleaned_up_image_url = cleaned_up_image_url.replace("https://storage.googleapis.com/fabmaster/cardfaces/2022-EVR/", "")
    cleaned_up_image_url = cleaned_up_image_url.replace("https://storage.googleapis.com/fabmaster/cardfaces/promos/", "")
    cleaned_up_image_url = cleaned_up_image_url.replace("https://storage.googleapis.com/fabmaster/cardfaces/2021-MON-CHN/", "")
    cleaned_up_image_url = cleaned_up_image_url.replace("https://storage.googleapis.com/fabmaster/cardfaces/2021-ELE-BRI/", "")

    file_name = "images/" + cleaned_up_image_url
    if exists(file_name):
        print(file_name + " already exists, skipping")
        return

    print("Downloading " + image_url + " to " + file_name)
    img_data = requests.get(image_url).content
    with open(file_name, 'wb') as handler:
        handler.write(img_data)

if not exists(images_dir_path):
    print(images_dir_path + " does not exist, creating it")
    makedirs(images_dir_path)

path = Path(__file__).parent / "../csvs/card.csv"
with path.open(newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
    next(reader)

    for row in reader:
        image_urls = [re.split(" – | - ", url.strip())[0].strip() for url in row[35].split(',')]
        for image_url in image_urls:
            download_image_from_url(image_url)

