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


errors = False

# Build a list of card types
type_filename = 'csvs/type.csv'
with open(type_filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter="\t")
    allowed_types = [x['Name'] for x in reader]

# Scan card.csv for errors
card_filename = 'csvs/card.csv'
with open(card_filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter="\t")
    for row in reader:
        card_types = re.split(',\s*', row['Types'])
        for card_type in card_types:
            if card_type not in allowed_types:
                print(f"Warning: unrecognized card type {card_type} in {card_filename} entry for "
                      f"{row['Name']}. Check your spelling or add this to {type_filename}.")
                errors = True

if errors:
    sys.exit(1)
