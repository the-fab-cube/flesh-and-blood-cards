import csv
from os.path import exists
from pathlib import Path

print("Generating artist.csv from card.json...")

# Compile list of unique artists from card.json
artists = set()

path = Path(__file__).parent / "../../csvs/english/card.csv"
with path.open(newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
    next(reader)

    for row in reader:
        artist_column=row[19]
        individual_artists=artist_column.split(',')
        for artist in individual_artists:
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