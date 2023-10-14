# Helper Scripts

## Python Scripts

- [Clean CSVs](/helper-scripts/clean-csvs/README.md)
- [Download All Images](/helper-scripts/download-all-images/README.md)
- [Generate Artists](/helper-scripts/generate-artists/README.md)
- [Generate CSV HTMLs](/helper-scripts/generate-artists/README.md)
- [Generate JSON](/helper-scripts/generate-json/README.md)
- [Generate JSON Schema HTMLs](/helper-scripts/generate-json-schema-htmls/README.md)
- [Generate SQL DB](/helper-scripts/generate-sql-db/README.md)
- [Validate References](/helper-scripts/validate-references/README.md)

## JavaScript Scripts

- [Generate Unique IDs](/helper-scripts/generate-unique-ids/README.md)
- [JSON Validation](/helper-scripts/json-validation/README.md)
- [Populate TCGPlayer Product IDs](/helper-scripts/populate-tcgplayer-product-ids/README.md)

## Bash Scripts

- `./clean-csvs.sh`
  - Shortcut to run the Clean CSVs script from the helper-scripts folder.
- `./download-all-images.sh`
  - Shortcut to run the Download All Images script from the helper-scripts folder.
- `./generate-artists.sh`
  - Shortcut to run the Generate Artists script from the helper-scripts folder.
- `./generate-htmls.sh`
  - Shortcut to run the Generate HTMLs script from the helper-scripts folder.
- `./generate-json.sh`
  - Shortcut to run the Generate JSON script from the helper-scripts folder.
- `./generate-unique-ids.sh`
  - Shortcut to run the Generate Unique IDs script from the helper-scripts folder.
- `./install-all-script-dependencies`
  - Shortcut to install all of the dependencies for the helper scripts in this folder. Assumes you have the appropriate versions of pyenv, nvm, and npm installed.
- `./populate-tcgplayer-product-ids.sh`
  - Shortcut to run the Populate TCGPlayer Product IDs script from the helper-scripts folder.
- `./pre-commit-scripts.sh`
  - Shortcut to run all of the scripts that should be run before committing from the helper-scripts folder, in this order:
    - Clean CSVs
    - Validate References
    - Generate Artists
    - Generate Artists
    - Generate Unique IDs
    - Generate JSON
    - Validate JSON
- `./validate-json.sh`
  - Shortcut to run the Validate JSON script from the helper-scripts folder.
