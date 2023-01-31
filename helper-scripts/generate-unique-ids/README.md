# Generate Unique IDs
Generate any missing unique IDs in the CSVs, to be used within the data set for easy association of objects. This skips over any existing IDs, since once created the ID should not be changed as that can break existing applications using the data set.

## Initial Setup
1. Install [nvm](https://github.com/nvm-sh/nvm#installing-and-updating).
3. Run `nvm use`.
2. Run `npm install` to install node modules.

## Running the Script
1. Run `npm run start` to run the unique ID generator.