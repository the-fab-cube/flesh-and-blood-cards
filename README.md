# Flesh and Blood Cards

## Table of Contents
1. [General Overview](#general-overview)
2. [Approach to Reprints/Editions](#approach-to-reprintseditions)
3. [Contributing](#contributing)
4. [Helper Scripts](#helper-scripts)
5. [Further Documentation](#further-documentation)
6. [Current Status on CSV Representation of Translated Cards](#current-status-on-csv-representation-of-translated-cards)
7. [Projects Using This Data Set](#projects-using-this-data-set)

## General Overview
This repo is intended as a comprehensive, open-source resource for representing all cards and sets from the Flesh and Blood TCG as JSON and CSV files.

The JSON files are the easiest format for general use, while the CSVs are meant to enable faster data entry while maintaining and contributing to this data set.

Please feel free to clone or fork the repo and generally use it for whatever projects you like. I put this together so the community doesn't have to keep re-entering the same data! I would absolutely appreciate any contributions if you notice any missing data or mistakes. :)

You can view the current JSON and CSV files through the web [here](https://the-fab-cube.github.io/flesh-and-blood-cards/).


## Approach to Reprints/Editions
This repo treats a unique card (name + pitch value) as 1 entity. A unique card can have multiple printings, foils, editions, etc, but is considered 1 entry in the data set.

A card's text and other data will always be based off the latest erratas and printings.

Similarly, a set is unique based on a setcode + name, and can have multiple editions, but is considered to be 1 entry within the data set.


## Contributing
This repo is primarily maintained by Tyler, but it's been a community effort finding bugs, suggesting and making improvements, and adding new card data! If you'd like to contribute, please take a look at [these instructions](/CONTRIBUTING.md).

## Helper Scripts
This project contains numerous helper scripts in order to help with data entry, generating JSON and HTML files, and spinning up PostgreSQL servers from the data. You can find more info on all of them [here](/helper-scripts/README.md).

## Further Documentation
You can find the more info on the following topics at these links:
* [Data Set Abbreviations](/documentation/abbreviations.md)
* [CSV Schemas](/documentation/csv-schemas.md)
* [JSON Schemas](/documentation/json-schemas.md)
* [LibreOffice Tricks](/documentation/libre-office-tricks.md)

## Current Status on CSV Representation of Translated Cards
If you are interested in helping transcribe the History Pack 1 Black Label cards, please comment [here](https://github.com/the-fab-cube/flesh-and-blood-cards/issues/118) to register your interest and I'll get in touch with you when efforts are ready to begin!

## Projects Using This Data Set
One of my favorite parts of maintaining this data set has been seeing all the community projects that have started using it. Here are all the projects that I know are using the data set! If your project is using it and I'm missing it, please leave an issue to let me know or open a PR to add your project to the list!

* fab-cards - [Repo](https://github.com/fabrary/fab-cards)
* FaB Eco Proxy - [Website](https://aongaro.github.io/fab-eco-proxy/) • [Repo](https://github.com/aongaro/fab-eco-proxy)
* Fabrary - [Website](https://fabrary.net/)
* Flesh and Blood TCG Analysis Environment - [Repo](https://github.com/HarrisonTotty/fab)
* Legendary Stories - [Website](https://legendarystories.net/) • [Repo](https://github.com/nathaneastwood/fablore)
* Talishar Online - [Website](https://talishar.net/) • [Repo](https://github.com/Talishar/Talishar)
* The Fab Cube - [Website](https://www.thefabcube.com/)