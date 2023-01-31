#!/usr/bin/env python3
import csv
import os
import re


def clean_hyphen_separated(data):
    """
    A very simple cleaner that just splits on whitespace-dash-whitespace, and joins on ' - '.
    Normalizes extra spacing on either side of the dash, as well as the use of dash characters
    other than the hyphen.
    """

    # \p{Pd} is a property which matches any hyphen or dash type of punctuation character. This
    # isn't available in the python standard library, but if you `pip install regex` and
    # `import regex as re` you will be able to use that instead of the bracketed character class.
    data = data.strip()
    fields = re.split(r'\s+[-–—]\s+', data)
    return ' - '.join(fields)


def clean_comma_separated(data):
    """
    Another very simple cleaner that just splits on comma-optionalwhitespace.
    """

    data = data.strip()
    fields = re.split(r',\s*', data)
    return ', '.join(fields)


def clean_hyphens_inside_commas(data):
    """
    A cleaner for fields like the "Image URLs" field in the card.csv file. This field is
    comma-separated, and each item of that is then hyphen-separated. This function cleans up extra
    or missing whitespace after the comma, and calls out to `clean_hyphen_separated` to deal with
    the dashes and whitespace around them.
    """

    # First, we split on the commas which separate the data for each printing of the card. They may
    # have erroneous spaces (or lack thereof).
    data = data.strip()
    entries = re.split(',\s*', data)

    # Then, each entry is hyphen-separated, but we need to make sure they are hyphens (not dashes of
    # any kind) and that they have exactly one space on each side.
    new_entries = []
    for entry in entries:
        new_entries.append(clean_hyphen_separated(entry))

    cleaned_data = ', '.join(new_entries)
    return cleaned_data


CLEANERS = {
    "Identifiers": clean_comma_separated,
    "Set Identifiers": clean_comma_separated,
    "Rarities": clean_comma_separated,
    "Types": clean_comma_separated,
    "Card Keywords": clean_comma_separated,
    "Abilities and Effects": clean_comma_separated,
    "Ability and Effect Keywords": clean_comma_separated,
    "Granted Keywords": clean_comma_separated,
    "Artists": clean_comma_separated,
    "Variations": clean_hyphens_inside_commas,
    "Variation Unique IDs": clean_hyphens_inside_commas,
    "Image URLs": clean_hyphens_inside_commas,
    "Editions": clean_comma_separated,
    "Edition Unique IDs": clean_hyphens_inside_commas,
}

def clean_fields(reader, fieldnames):
    """
    This function handles a single CSV file, iterating over the rows, passing any fields to the
    appropriate cleaners, and finally returning the cleaned list of dictionaries.
    """

    cleaned_data = []
    for row in reader:
        for key in row:
            # Always normalize smart quotes
            row[key] = row[key].replace('“','"').replace('”','"')
            row[key] = row[key].replace('‘',"'").replace('’',"'")

            if key in CLEANERS:
                row[key] = CLEANERS[key](row[key])
        cleaned_data.append(row)
    return cleaned_data

def process_file(filename):
    """
    This function handles the file I/O for a single CSV file, and passes the data to `clean_fields`
    to be cleaned.
    """

    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter="\t")
        fieldnames = reader.fieldnames
        cleaned_data = clean_fields(reader, fieldnames)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in cleaned_data:
            writer.writerow(row)


# Add any additional files to be cleaned here.
csvs_path = 'csvs'
for language_name in os.listdir(csvs_path):
    language_path = os.path.join(csvs_path, language_name)
    if os.path.isdir(language_path):
        for file_name in os.listdir(language_path):
            if file_name.endswith('.csv'):
                file_path = os.path.join(language_path, file_name)
                process_file(file_path)
