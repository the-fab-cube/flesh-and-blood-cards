import csv
import json
from os.path import exists
from pathlib import Path

print("Generating artist.csv from card.json...")

# Compile list of unique artists from card.json
artists = set()

path = Path(__file__).parent / "../../json/english/card.json"
with path.open(newline='') as jsonfile:
    card_array = json.load(jsonfile)

    for card in card_array:
        for printing in card['printings']:
            artist = printing['artist']
            artists.add(artist.strip())

# Sort the artists
artists_sorted = sorted(artists, key=str.casefold)

# Output the sorted list of unique artists as a CSV
path = Path(__file__).parent / "../../csvs/english/artist.csv"
with path.open('w', newline='\n') as csvout:
    writer = csv.writer(csvout)

    # Add title row
    writer.writerow(["Name"])

    for artist in artists_sorted:
        writer.writerow([artist])

print("Successfully generated artist.csv")