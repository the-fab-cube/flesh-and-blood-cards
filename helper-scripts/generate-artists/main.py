import csv
from os.path import exists
from pathlib import Path

print("Generating artist.csv from card.csv...")

artists = set()

path = Path(__file__).parent / "../../csvs/card.csv"
with path.open(newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
    next(reader)

    for row in reader:
        artist_column=row[18]
        individual_artists=artist_column.split(',')
        for artist in individual_artists:
            artists.add(artist.strip())

artists_sorted = sorted(artists, key=str.casefold)

path = Path(__file__).parent / "../../csvs/artist.csv"
with path.open('w', newline='\n') as csvout:
    writer = csv.writer(csvout)

    # Add title row
    writer.writerow(["Name"])

    for artist in artists_sorted:
        writer.writerow([artist])

print("Successfully generated artist.csv")