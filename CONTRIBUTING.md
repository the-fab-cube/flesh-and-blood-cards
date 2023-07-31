# Contributing

Welcome!

If you're reading this, hopefully you're interested in helping out with the maintenance of this data set by adding missing info or fixing mistakes I've made while entering the data. If you are interested, please continue reading for instructions on how to help. Otherwise, I hope this data set has been helpful to you, and even if you have no interest in contributing, if you notice any mistakes or have suggestions, please [create an issue](https://github.com/the-fab-cube/flesh-and-blood-cards/issues/new) so I or someone else can fix it!

## Getting Started
1. Install the dependencies for the various helper-scripts. If you'd like a quick way to install all of the dependencies, you can run the [install-all-script-dependencies bash script](/helper-scripts/README.md). You will just need to make sure that you have the following installed before you run the script:
    * [pyenv](https://github.com/pyenv/pyenv)
    * [poetry](https://python-poetry.org/)
        * I recommend using `pyenv exec pip install poetry` after installing pyenv.
    * [nvm](https://github.com/nvm-sh/nvm#installing-and-updating)
2. Find an Issue you'd like to work on.
    * You can find a list of open issues [here](https://github.com/the-fab-cube/flesh-and-blood-cards/issues) and a summary of data entry milestones [here](https://github.com/flesh-cube/flesh-and-blood-cards/milestones).
3. Check to make sure no one is assigned to the Issue.
4. If no one is working on it, please leave a comment mentioning you would like to work on it and I will assign you to the Issue.
5. When you are done with your work, create a PR to this repo's develop branch and tag the issue you were working on. I'll review it and if it's good to go, approve it!


## Entering English CSV Data
Data should be entered directly into the appropriate CSV. After entering the data, please run the [pre-commit-script bash script](/helper-scripts/README.md), which will take care of validating and generating the various CSV and JSON files. Alternatively, you can enable the pre-commit hooks so that these scrpits run whenever you commit. If you're interested in that, see the Running Git Hooks with Pre-Commit section below.

NOTE: You can find the CSV schema data [here](/documentation/csv-schemas.md).

## Entering Non-English CSV Data
If you are entering data for languages other than English, first go find the unique ID for the particular piece of data you are adding in English, if it exists. Make a new line in the corresponding CSV in the language you'd like to add that data to, put the unique ID in, and then fill out the rest of the missing info like you would for English.

It is worth noting that for cards, the CSV has much fewer columns than it does in English. That is because the JSON generator uses the English data as a source of truth, and will automatically pull what it can from the English data! So just fill out what's missing and it should be good. If the JSON generator is missing a translation for a keyword, type, etc., it will throw an exception and tell you what needs fixed. If you run into any issues with this, just open a PR and explain what's going on and I can help out!

## Running Git Hooks with Pre-Commit
You can install git hooks to clean and validate the CSV data using pre-commit. To do so, follow these steps:

1. Install [pre-commit](https://pre-commit.com/)
2. Run `pre-commit install`
3. The git hook should now run every time you make a commit!
4. You can also optionally manually run the git hook with `pre-commit run`

## Other Data Requirements
- All image links must be from LSS' site.
- Functional text must be the latest oracle text.
- CSVs should be ordered by name alphabetically, with the exception of card/set printings, which should be ordered by card/set id.
- Cards that have already been entered into the CSVs should not change ordering drastically through PRs. (I may re-organize them in the future, but keeping them consistent helps keep PRs easier to review!)

Thanks again for helping out! Please let me know if you have any questions or if I could make anything clearer!

-- Tyler
