const fs = require("fs");
const csv = require('csv');
const helper = require('../helper-functions')

// Set an index to null to omit generation for the associated unique ID
const generateSetUniqueIds = (language, editionsIndex, editionUniqueIdsIndex) => {
    const inputCSV = `../../csvs/${language}/set.csv`
    const outputCSV = `./temp-${language}-set.csv`

    const readStream = fs.createReadStream(inputCSV)
    const writeStream = fs.createWriteStream(outputCSV)
    const csvStream = csv.parse({ delimiter: "\t" })
    const stringifier = csv.stringify({ delimiter: "\t" });

    const capitalizedLanguage = helper.capitalizeFirstLetter(language)

    const csvStreamFinished = function (editionIdsAdded) {
        fs.renameSync(outputCSV, inputCSV)
        console.log(`Unique ID generation completed for ${capitalizedLanguage} sets with ${editionIdsAdded} new edition IDs!`)
    }

    var headerRead = false
    var editionIdsAdded = 0

    csvStream.on("data", function(data) {
        // Skip header
        if (!headerRead) {
            headerRead = true
            stringifier.write(data)
            return
        }

        // Edition Unique ID
        if (editionsIndex !== null && editionsIndex !== undefined && editionUniqueIdsIndex !== null && editionUniqueIdsIndex !== undefined) {
            // current edition unique IDs data
            var editions = data[editionsIndex]
                .split(",")
                .filter(x => x.trim() !== '' && x !== undefined)
                .map(x => x.trim())

            var existingEditionUniqueIDs = {}
            data[editionUniqueIdsIndex]
                .split(",")
                .filter(x => x.trim() !== '' && x !== undefined)
                .forEach(x => {
                    var splitEdition = x.trim().split(RegExp(" — | – | - "))

                    if (splitEdition.length !== 2) {
                        return
                    }

                    var editionUniqueId = splitEdition[0].trim()
                    var edition = splitEdition[1].trim()

                    existingEditionUniqueIDs[edition] = editionUniqueId
                })

            // generate unique IDs for editions
            var editionUniqueIds = editions.map(edition => {
                var editionUniqueId = existingEditionUniqueIDs[edition]
                var editionUniqueIdExists = editionUniqueId !== undefined

                if (!editionUniqueIdExists) {
                    console.log(`Generating unique ID for ${capitalizedLanguage} edition ${edition}`)
                    editionIdsAdded += 1
                    editionUniqueId = helper.customNanoId()
                } else {
                    // console.log(`No new unique ID needed for ${capitalizedLanguage} edition ${edition}`)
                }

                return editionUniqueId + " – " + edition
            });

            data[editionUniqueIdsIndex] = editionUniqueIds.join(", ")
        }

        // save CSV row
        stringifier.write(data)
    })
    .on('end', () => {
        csvStreamFinished(editionIdsAdded)
    })
    .on("error", function (error) {
        console.log(error.message)
    })

    stringifier.pipe(writeStream)
    readStream.pipe(csvStream)
}

module.exports = {
    generateSetUniqueIds
}