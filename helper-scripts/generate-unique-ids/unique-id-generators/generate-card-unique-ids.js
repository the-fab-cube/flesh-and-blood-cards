const fs = require("fs");
const csv = require('csv');
const helper = require('../helper-functions')

// Set an index to null to omit generation for the associated unique ID
const generateCardUniqueIds = (language, uniqueIdIndex, cardIdIndex, variationsIndex, variationUniqueIdsIndex) => {
    const inputCSV = `../../csvs/${language}/card.csv`
    const outputCSV = `./temp-${language}-card.csv`

    const readStream = fs.createReadStream(inputCSV)
    const writeStream = fs.createWriteStream(outputCSV)
    const csvStream = csv.parse({ delimiter: "\t" })
    const stringifier = csv.stringify({ delimiter: "\t" });

    const capitalizedLanguage = helper.capitalizeFirstLetter(language)

    const csvStreamFinished = function (cardIdsAdded, variationIdsAdded) {
        fs.renameSync(outputCSV, inputCSV)
        console.log(`Unique ID generation completed for ${capitalizedLanguage} cards with ${cardIdsAdded} new card IDs and ${variationIdsAdded} new variation IDs!`)
    }

    var headerRead = false
    var cardIdsAdded = 0
    var variationIdsAdded = 0

    csvStream.on("data", function(data) {
        // Skip header
        if (!headerRead) {
            headerRead = true
            stringifier.write(data)
            return
        }

        // Card Unique ID
        if (uniqueIdIndex !== null && uniqueIdIndex !== undefined && cardIdIndex !== null && cardIdIndex !== undefined) {
            // current card unique ID data
            var uniqueID = data[uniqueIdIndex]
            var cardID = data[cardIdIndex]

            var uniqueIdExists = uniqueID.trim() !== ''

            // generate unique ID for card
            if (!uniqueIdExists) {
                console.log(`Generating unique ID for ${capitalizedLanguage} card ${cardID}`)
                cardIdsAdded += 1
                data[uniqueIdIndex] = helper.customNanoId()
            } else {
                // console.log(`No new unique ID needed for ${capitalizedLanguage} card ${cardID}`)
            }
        }

        // Variation Unique ID
        if (variationsIndex !== null && variationsIndex !== undefined && variationUniqueIdsIndex !== null && variationUniqueIdsIndex !== undefined) {
            // current variation unique IDs data
            var variations = data[variationsIndex]
                .split(",")
                .filter(x => x.trim() !== '' && x !== undefined)
                .map(x => {
                    var splitVariation = x.trim().split(RegExp(" — | – | - "))
                    var variation = splitVariation[1] + " - " + splitVariation[2]

                    if (splitVariation.length > 3) {
                        variation +=  " - " + splitVariation[3]
                    }

                    return variation
                })

            var existingVariationUniqueIDs = {}
            data[variationUniqueIdsIndex]
                .split(",")
                .filter(x => x.trim() !== '' && x !== undefined)
                .forEach(x => {
                    var splitVariation = x.trim().split(RegExp(" — | – | - "))

                    if (splitVariation.length < 3) {
                        return
                    }

                    var variationUniqueId = splitVariation[0]
                    var variation = splitVariation[1] + " - " + splitVariation[2]

                    if (splitVariation.length > 3) {
                        variation +=  " - " + splitVariation[3]
                    }

                    existingVariationUniqueIDs[variation] = variationUniqueId
                })

            // generate unique IDs for variations
            var variationUniqueIds = variations.map(variation => {
                var variationUniqueId = existingVariationUniqueIDs[variation]
                var variationUniqueIdExists = variationUniqueId !== undefined

                if (!variationUniqueIdExists) {
                    console.log(`Generating unique ID for ${capitalizedLanguage} variation ${variation}`)
                    variationIdsAdded += 1
                    variationUniqueId = helper.customNanoId()
                } else {
                    // console.log(`No new unique ID needed for ${capitalizedLanguage} variation ${variation}`)
                }

                return variationUniqueId + " - " + variation
            });

            data[variationUniqueIdsIndex] = variationUniqueIds.join(", ")
        }

        // save CSV row
        stringifier.write(data)
    })
    .on('end', () => {
        csvStreamFinished(cardIdsAdded, variationIdsAdded)
    })
    .on("error", function (error) {
        console.log(error.message)
    })

    stringifier.pipe(writeStream)
    readStream.pipe(csvStream)
}

module.exports = {
    generateCardUniqueIds
}