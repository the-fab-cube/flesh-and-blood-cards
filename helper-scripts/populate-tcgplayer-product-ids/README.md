# Populate TCGPlayer Product IDs

Fetch all TCGPlayer Product Ids for the specified TCGPlayer group and insert any missing product IDs for a specific set into the CSVs.

## Initial Setup

1. Install [nvm](https://github.com/nvm-sh/nvm#installing-and-updating).
2. Run `nvm use`.
3. Run `npm install` to install node modules.

## Running the Script

1. Please note that you'll need to have access to TCGPlayer's API and a valid Access Token. You can find more info [here](https://docs.tcgplayer.com/docs/getting-started).
2. Get the tcgplayerGroupId (I suggest doing a text search on TCGCSV's [Flesh and Blood group CSV](https://tcgcsv.com/62/groups)) and setId for the set you wish to populate.
3. Run `npm run start [tcgplayerAccessToken] [tcgplayerGroupId] [setId]` to run the script to fetch the productIds for the TCGPlayer group id (limiting matching to the setId printings in the CSV).
