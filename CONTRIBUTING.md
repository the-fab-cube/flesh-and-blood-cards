# Contributing

Welcome!

If you're reading this, hopefully you're interested in helping out with the maintenance of this data set by adding missing info or fixing mistakes I've made while entering the data. If you are interested, please continue reading for instructions on how to help. Otherwise, I hope this data set has been helpful to you, and even if you have no interest in contributing, if you notice any mistakes or have suggestions, please [create an issue](https://github.com/the-fab-cube/flesh-and-blood-cards/issues/new) so I or someone else can fix it!

## Getting Started
1. Find an Issue you'd like to work on.
    * You can find a list of open issues [here](https://github.com/the-fab-cube/flesh-and-blood-cards/issues) and a summary of data entry milestones [here](https://github.com/flesh-cube/flesh-and-blood-cards/milestones).
2. Check to make sure no one is assigned to the Issue.
3. If no one is working on it, please leave a comment mentioning you would like to work on it and I will assign you to the Issue.
4. When you are done with your work, create a PR to this repo's develop branch and tag the issue you were working on. I'll review it and if it's good to go, approve it!


## Entering English CSV Data
I have LibreOffice files in the repo for easy editing. It is okay if you do not use them, I will update them with any changes other people make without using LibreOffice, but they are there for convenience. To use them, just open the .ods file and edit, and then when done, export the file as a .csv to the appropriate language's folder in the csvs folder with Save As, making sure to choose Tabs as the delimiter and " as the string indicator.

After entering the data, please run the [pre-commit-script bash script](/helper-scripts/README.md), which will take care of generating the various JSON, CSV, and HTML files. After running this, if you are using the LibreOffice ODS files and added a new card and/or card variation, please copy the newly generated unique ID back over to the ODS file so data isn't lost when you export the ODS file to CSV again in the future.

NOTE: You can find the CSV schema data [here](/documentation/csv-schemas.md).

## Entering Non-English CSV Data
If you are entering data for languages other than English, first go find the unique ID for the particular piece of data you are adding in English, if it exists. Make a new line in the corresponding CSV in the language you'd like to add that data to, put the unique ID in, and then fill out the rest of the missing info like you would for English.

It is worth noting that for cards, the CSV has much fewer columns than it does in English. That is because the JSON generator uses the English data as a source of truth, and will automatically pull what it can from the English data! So just fill out what's missing and it should be good. If the JSON generator is missing a translation for a keyword, type, etc., it will throw an exception and tell you what needs fixed. If you run into any issues with this, just open a PR and explain what's going on and I can help out!

Finally, it is also worth noting that sets may not have an existing unique ID in English. For example, History Pack - Black Label was not printed in English. In this case, just leave the column empty and run the `generate-unique-ids` script. It should create a new unique ID in the CSV, and all you'll have to do is copy that back to the ODS file if you're using it.

(Please note that if you are adding data for a set in multiple languages at once, you will need to run the unique ID generator for **one** language and then use that unique ID for the set in the other languages!)

## Running Git Hooks with Pre-Commit
You can install git hooks to clean and validate the CSV data using pre-commit. To do so, follow these steps:

1. Install [pre-commit](https://pre-commit.com/)
2. Run `pre-commit install`
3. The git hook should now run every time you make a commit!
4. You can also optionally manually run the git hook with `pre-commit run`

## Other Data Requirements
- All image links must be from LSS' site.
- Functional text must be the latest oracle text.
- Cards that have already been entered into the CSVs should not change ordering drastically through PRs. (I may re-organize them in the future, but keeping them consistent helps keep PRs easier to review!)

Thanks again for helping out! Please let me know if you have any questions or if I could make anything clearer!

-- Tyler
