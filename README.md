# Flesh and Blood Cards
[Patreon](https://www.patreon.com/TheFabCube) &#183; [Discord](https://discord.gg/NRKZsmEJm2) &#183; [Releases](https://github.com/the-fab-cube/flesh-and-blood-cards/releases)

## Table of Contents
1. [General Overview](#general-overview)
2. [Approach to Reprints/Editions](#approach-to-reprintseditions)
3. [Approach to Versioning](#approach-to-versioning)
4. [Approach to Languages](#approach-to-languages)
5. [Changelogs and Contribution Credit](#changelogs-and-contribution-credit)
6. [Contributing](#contributing)
7. [Helper Scripts](#helper-scripts)
8. [Further Documentation](#further-documentation)
9. [Current Status on CSV Representation of Translated Cards](#current-status-on-csv-representation-of-translated-cards)
10. [Projects Using This Data Set](#projects-using-this-data-set)

## General Overview
This repo is intended as a comprehensive, open-source resource for representing all cards and sets from the Flesh and Blood TCG as JSON and CSV files.

The JSON files are the easiest format for general use, while the CSVs are meant to enable faster data entry while maintaining and contributing to this data set.

Please feel free to clone or fork the repo and generally use it for whatever projects you like. I put this together so the community doesn't have to keep re-entering the same data! I would absolutely appreciate any contributions if you notice any missing data or mistakes. :)

You can view the current JSON and CSV files through the web [here](https://the-fab-cube.github.io/flesh-and-blood-cards/).


## Approach to Reprints/Editions
This repo treats a unique card (name + pitch value) as 1 entity. A unique card can have multiple printings, foils, editions, etc, but is considered 1 entry in the data set.

A card's text and other data will always be based off the latest erratas and printings.

Similarly, a set is unique based on a setcode + name, and can have multiple editions, but is considered to be 1 entry within the data set.

All cards, printings, sets, set editions, and other data in the data set is also assigned a unique generated unique_id when they are added that is consistent throughout the data set. Once a unique_id is added to the data set, it will never be changed and should be a stable way to refer to that particular piece of data. (NOTE: By "will never be changed" I mean "if this is changed, something went horribly wrong and I need to revert the unique_id back to its original value, and if you notice this please let me know!".)


## Approach to Versioning
To the best of my ability, I attempt to follow [Semantic Versioning](https://semver.org/) when releasing versions of this data set. You can find all released versions [here](https://github.com/the-fab-cube/flesh-and-blood-cards/releases).

I try to increment version numbers with this general logic:

* Major - The schema for the CSV / JSON was changed, large file organizational changes were made, etc.
* Minor - New data was added, new scripts were added or updated, etc. (Scripts receiving breaking changes are not always guaranteed to warrant a major patch bump, use with caution!)
* Patch - Errors in the data or helper scripts were fixed

If you'd like a stable experience, please use the main branch and pin a specific tagged version. I try to keep the develop branch as clean as possible, but even that is broken or has big changes in-flight from time to time. For bigger changes to the data set or during spoiler seasons, I spin off feature branches to work in. You are welcome to use them while I am working on them, but please be aware things can break at any time!

Unlike many code packages, I do not go back and support past major/minor releases with bugfixes, so if you want the most up-to-date data, you will always need to be on the latest version, even if that version has breaking changes. The versioning system is purely to give you a heads up so that you don't update and find your project blowing up unexpectedly!

## Approach to Languages
This data set currently supports the following languages:
- English
- French
- German
- Italian
- Spanish

In this data set, English is considered the "default" language. All cards, keywords, types, etc. should be added in English first (for sets, this is even if the set has never been printed in English). These are all contained within the `english/` subfolders of the `json/` and `csvs/`.

All other languages have their own subfolders with translated data, with unique_ids corresponding to the English data. These include:
- Abilities
- Cards
- Keywords
- Types

There are three types of data that are handled somewhat differently in other languages.

Each language folder has its own artist data to account for the possibility that a card variation in one language has an artist that another language does not.

While the card data should be consistent across all languages with just the text being translated, the card printings are not. Each languages' card printing data only has data on the printings that card has had in that language.

Similarly, each languages' set printings only contain the printings of the set for that language.


## Changelogs and Contribution Credit
I include text changelogs for more information on when something changed and to help me remember what changed when I release new versions and need to write-up patch notes for them. The changelog for the actual data is at the root of the repo [here](/changelog.txt), and the changelogs for the various scripts can all be found at the root of each script's folder.

I do my best to include the usernames of who submitted specific data updates or bugfixes (or who even just notified me of an issue). If I missed crediting you, please let me know so I can fix it! Conversely, if I've credited you and you wish for me to remove your username or update it, please also let me know!


## Contributing
This repo is primarily maintained by Tyler ([luceleaftea](https://github.com/luceleaftea)), but it's been a community effort finding bugs, suggesting and making improvements, and adding new card data! If you'd like to contribute, please take a look at [these instructions](/CONTRIBUTING.md).

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
* FaB Proxy - [Website](https://fabproxy.com/)
* Fabrary - [Website](https://fabrary.net/)
* Flesh and Blood TCG Analysis Environment - [Repo](https://github.com/HarrisonTotty/fab)
* Legendary Stories - [Website](https://legendarystories.net/) • [Repo](https://github.com/nathaneastwood/fablore)
* Rules of Rathe - [Splash Page](https://rulesofrathe.com/) • [iOS](https://apps.apple.com/de/app/rules-of-rathe/id1585516530) • [Android](https://play.google.com/store/apps/details?id=com.rulesofrathe&pli=1) • [Website](https://rulesofrathe.com/m/)
* Talishar Online - [Website](https://talishar.net/) • [Repo](https://github.com/Talishar/Talishar)
* The Fab Cube - [Website](https://www.thefabcube.com/)