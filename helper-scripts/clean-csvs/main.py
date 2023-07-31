#!/usr/bin/env python3
import csv
import os
import re


def clean_hyphen(data):
    """
    A very simple cleaner that just splits on dash characters, and joins on '-'.
    Normalizes the use of dash characters other than the hyphen.
    """

    # \p{Pd} is a property which matches any hyphen or dash type of punctuation character. This
    # isn't available in the python standard library, but if you `pip install regex` and
    # `import regex as re` you will be able to use that instead of the bracketed character class.
    data = data.strip()
    fields = re.split(r'[-–—]', data)
    return '-'.join(fields)


def clean_comma_separated(data):
    """
    Another very simple cleaner that just splits on comma-optionalwhitespace.
    """

    data = data.strip()
    fields = re.split(r',\s*', data)
    return ', '.join(fields)


CLEANERS = {
    "Types": clean_comma_separated,
    "Card Keywords": clean_comma_separated,
    "Abilities and Effects": clean_comma_separated,
    "Ability and Effect Keywords": clean_comma_separated,
    "Granted Keywords": clean_comma_separated,
    "Functional Text": clean_hyphen,
    "Flavor Text": clean_hyphen,
    "Type Text": clean_hyphen,
    "Description": clean_hyphen,
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
            if row[key] is not None:
                row[key] = row[key].replace('“','"').replace('”','"')
                row[key] = row[key].replace('‘',"'").replace('’',"'")

                # Always normalize non-normal spaces
                row[key] = row[key].replace(' '," ")

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
csvs_path = '../../csvs'
for language_name in os.listdir(csvs_path):
    language_path = os.path.join(csvs_path, language_name)
    if os.path.isdir(language_path):
        for file_name in os.listdir(language_path):
            if file_name.endswith('.csv'):
                file_path = os.path.join(language_path, file_name)
                process_file(file_path)
