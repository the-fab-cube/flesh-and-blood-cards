#!/usr/bin/env python3
import csv
import re
import sys


"""
validate_references.py - verify that values which refer to other files are present and typed
correctly.

This script scans the csv files and looks for references to other files (like the Types column in
card.csv and ensures that each value is actually present in the referenced CSV.

If it detects an error, it will report a filename and line number, and return non-zero to allow
pre-commit to detect a failure.
"""

print("Validating CSV references...\n")

errors = False

# Build a list of art variations
variation_filename = '../../csvs/english/art-variation.csv'
with open(variation_filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter="\t")
    allowed_variations = [x['Shorthand'] for x in reader]

# Build a list of card types
type_filename = '../../csvs/english/type.csv'
with open(type_filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter="\t")
    allowed_types = [x['Name'] for x in reader]

# Build a list of editions
edition_filename = '../../csvs/english/edition.csv'
with open(edition_filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter="\t")
    allowed_editions = [x['Shorthand'] for x in reader]

# Build a list of foilings
foiling_filename = '../../csvs/english/foiling.csv'
with open(foiling_filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter="\t")
    allowed_foilings = [x['Shorthand'] for x in reader]

# Build a list of rarities
rarity_filename = '../../csvs/english/rarity.csv'
with open(rarity_filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter="\t")
    allowed_rarities = [x['Shorthand'] for x in reader]

# Build a list of sets
set_filename = '../../csvs/english/set.csv'
with open(set_filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter="\t")
    allowed_sets = {x['Identifier']:x for x in reader}

# Build a list of set printings
set_printing_filename = '../../csvs/english/set-printing.csv'
with open(set_printing_filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter="\t")
    allowed_set_printings = {x['Unique ID']:x for x in reader}

# Build a list of card unique_ids
card_filename = '../../csvs/english/card.csv'
with open(card_filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter="\t")
    allowed_card_unique_ids = []

    for row in reader:
        allowed_card_unique_ids.append(row['Unique ID'])

# Build a list of card printing unique_ids
card_printing_filename = '../../csvs/english/card-printing.csv'
with open(card_printing_filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter="\t")
    allowed_card_printing_unique_ids = []

    for row in reader:
        allowed_card_printing_unique_ids.append(row['Unique ID'])

# Scan card legality CSVs for errors
legality_csv_filenames = [
    '../../csvs/english/banned-blitz.csv',
    '../../csvs/english/banned-cc.csv',
    '../../csvs/english/banned-commoner.csv',
    '../../csvs/english/banned-upf.csv',
    '../../csvs/english/living-legend-blitz.csv',
    '../../csvs/english/living-legend-cc.csv',
    '../../csvs/english/suspended-blitz.csv',
    '../../csvs/english/suspended-cc.csv',
    '../../csvs/english/suspended-commoner.csv',
    '../../csvs/english/restricted-ll.csv',
]

for legality_filename in legality_csv_filenames:
    legality_filename = '../../csvs/english/banned-blitz.csv'
    with open(legality_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter="\t")
        for row in reader:
            card_unique_id = row['Card Unique ID']
            if card_unique_id not in allowed_card_unique_ids:
                print(f"Warning: unrecognized card variation unique id {card_unique_id} in {legality_filename} entry for "
                        f"{row['Card Name']} - {row['Card Pitch']}. Check your spelling or add this to {card_filename}.")
                errors = True

# Scan card.csv for errors
card_filename = '../../csvs/english/card.csv'
with open(card_filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter="\t")
    for row in reader:
        # TODO: Duplicate Unique ID

        card_types = re.split(',\s*', row['Types'])
        for card_type in card_types:
            if card_type not in allowed_types:
                print(f"Warning: unrecognized card type {card_type} in {card_filename} entry for "
                      f"{row['Name']}. Check your spelling or add this to {type_filename}.")
                errors = True

# Scan card-printing.csv for errors
card_printing_filename = '../../csvs/english/card-printing.csv'
with open(card_printing_filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter="\t")
    for row in reader:
        # TODO: Duplicate Unique ID

        card_printing_summary = f"{row['Card ID']} (Edition: {row['Edition']} - Foiling: {row['Foiling']} - Art Variation: {row['Art Variation']})"

        # Set Printing Unique ID
        set_printing_unique_id = row['Set Printing Unique ID']
        this_set_printing = None
        try:
            this_set_printing = allowed_set_printings[set_printing_unique_id]
        except KeyError:
            print(f"Warning: unrecognized set printing unique id {set_printing_unique_id} in {card_printing_filename} entry for "
                  f"{card_printing_summary}. Check your spelling or add this to {set_printing_filename}.")
            errors = True

        # Set ID
        set_id = row['Set ID']
        if set_id not in allowed_sets:
            print(f"Warning: unrecognized set {set_id} in {card_printing_filename} entry for "
                  f"{card_printing_summary}. Check your spelling or add this to {set_filename}.")
            errors = True

        # Card ID
        card_id = row['Card ID']
        set_id_from_card_id = card_id[0:3]
        if set_id != set_id_from_card_id:
            print("Warning: card has a card ID for a set that isn't associated with that "
                  f"card. Found {card_id} for {card_printing_summary} in {card_printing_filename}. Check "
                  "this entry for consistency.")
            errors = True

        if this_set_printing:
            # Weird check of this_set_printing because I /don't/ want to catch exceptions anymore
            if not (this_set_printing['Start Card Id'] <= card_id <= this_set_printing['End Card Id']):
                print(f"Warning: card ID out of range for this set printing. Found {card_id} in "
                        f"{card_printing_filename} entry for {card_printing_summary} but {set_printing_filename} gives "
                        f"range {this_set_printing['Start Card Id']} - {this_set_printing['End Card Id']}.")
                errors = True

        # Art Variation
        variation = row['Art Variation']
        if variation != '' and variation not in allowed_variations:
            print(f"Warning: unrecognized variation {variation} in {card_printing_filename} entry for "
                  f"{card_printing_summary}. Check your spelling or add this to {variation_filename}.")
            errors = True

        # Edition
        edition = row['Edition']
        set_printing_edition = this_set_printing['Edition']
        if edition not in allowed_editions:
            print(f"Warning: unrecognized edition {edition} in {card_printing_filename} entry for "
                  f"{card_printing_summary}. Check your spelling or add this to {edition_filename}.")
            errors = True
        if set_printing_edition != edition:
            print(f"Warning: edition {edition} in {card_printing_filename} entry for "
                  f"{card_printing_summary} does not match the associated set's edition of {set_printing_edition}.")
            errors = True

        # Foiling
        foiling = row['Foiling']
        if foiling not in allowed_foilings:
            print(f"Warning: unrecognized foiling {foiling} in {card_printing_filename} entry for "
                  f"{card_printing_summary}. Check your spelling or add this to {foiling_filename}.")
            errors = True

        # Rarity
        rarity = row['Rarity']
        if rarity not in allowed_rarities:
            print(f"Warning: unrecognized rarity {rarity} in {card_printing_filename} entry for "
                  f"{card_printing_summary}. Check your spelling or add this to {rarity_filename}.")
            errors = True


# Scan card-face-association.csv for errors
card_face_association_filename = '../../csvs/english/card-face-association.csv'
with open(card_face_association_filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter="\t")
    for row in reader:
        front_card_printing_unique_ids = re.split(',\s*', row['Front Card Printing Unique ID'])
        for unique_id in front_card_printing_unique_ids:
            if unique_id not in allowed_card_printing_unique_ids:
                print(f"Warning: unrecognized card printing unique id {unique_id} in {card_face_association_filename} entry for "
                      f"{row['Front Card Name']} {row['Front Card Printing']}. Check your spelling or add this to {card_filename}.")
                errors = True

        back_card_printing_unique_ids = re.split(',\s*', row['Back Card Printing Unique ID'])
        for unique_id in back_card_printing_unique_ids:
            if unique_id not in allowed_card_printing_unique_ids:
                print(f"Warning: unrecognized card printing unique id {unique_id} in {card_face_association_filename} entry for "
                      f"{row['Back Card Name']} {row['Back Card Printing']}. Check your spelling or add this to {card_filename}.")
                errors = True


# Scan card-reference.csv for errors
card_reference_filename = '../../csvs/english/card-reference.csv'
with open(card_reference_filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter="\t")
    for row in reader:
        card_unique_id = re.split(',\s*', row['Card Unique ID'])
        for unique_id in card_unique_id:
            if unique_id not in allowed_card_unique_ids:
                print(f"Warning: unrecognized card unique id {unique_id} in {card_reference_filename} entry for "
                      f"{row['Card Name']} ({row['Card Pitch']}). Check your spelling or add this to {card_filename}.")
                errors = True

        referenced_card_unique_id = re.split(',\s*', row['Referenced Card Unique ID'])
        for unique_id in referenced_card_unique_id:
            if unique_id not in allowed_card_unique_ids:
                print(f"Warning: unrecognized card unique id {unique_id} in {card_reference_filename} entry for "
                      f"{row['Referenced Card Name']} ({row['Referenced Card Pitch']}). Check your spelling or add this to {card_filename}.")
                errors = True


if errors:
    print("\n")
    sys.exit(1)
