# Generate Unique IDs
Generate any missing unique IDs in the CSVs, to be used within the data set for easy association of objects. This skips over any existing IDs, since once created the ID should not be changed as that can break existing applications using the data set.

## Initial Setup
1. Install [nvm](https://github.com/nvm-sh/nvm#installing-and-updating).
3. Run `nvm use`.
2. Run `npm install` to install node modules.

## Running the Script
1. Run `./node_modules/pajv/index.js validate -s <json-schema-filepath> -d <json-to-validate-filepath>` to run the `pajv` JSON schema validator with the given JSON and schema files.

    OR

2. Run `./validate-json.sh` to run the `pajv` JSON schema validator on all of the existing JSON files.