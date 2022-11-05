import csv
from os.path import exists
from pathlib import Path

artists = set()

path = Path(__file__).parent / "../csvs/card.csv"
with path.open(newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
    next(reader)

    for row in reader:
        artists.add(row[2])

artists_sorted = sorted(artists)

path = Path(__file__).parent / "../csvs/artists.csv"
with path.open('w', newline='\n') as csvout:
    writer = csv.writer(csvout)
    for artist in artists_sorted:
        writer.writerow([artist])