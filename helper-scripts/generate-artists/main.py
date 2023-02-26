import csv
from os.path import exists
from pathlib import Path
import re

def create_artists_csv_from_card_csv(language, artist_column_index):
    print(f"Generating {language} artist.csv from {language} card.json...")

    # Compile list of unique artists from all languages' card.csv
    artists = set()

    path = Path(__file__).parent / f"../../csvs/{language}/card.csv"
    with path.open(newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(reader)

        for row in reader:
            artist_column=row[artist_column_index]
            individual_artists=artist_column.split(',')
            for artist in individual_artists:
                artists.add(re.split(r'\s+[-–—]\s+', artist)[0].strip())

    # Sort the artists
    artists_sorted = sorted(artists, key=str.casefold)

    # Output the sorted list of unique artists as a CSV
    path = Path(__file__).parent / f"../../csvs/{language}/artist.csv"
    with path.open('w', newline='') as csvout:
        writer = csv.writer(csvout, lineterminator="\n")

        # Add title row
        writer.writerow(["Name"])

        for artist in artists_sorted:
            writer.writerow([artist])

    print(f"Successfully generated {language} artist.csv")



create_artists_csv_from_card_csv("english", 19)
create_artists_csv_from_card_csv("french", 8)
create_artists_csv_from_card_csv("german", 8)
create_artists_csv_from_card_csv("italian", 8)
create_artists_csv_from_card_csv("spanish", 8)
