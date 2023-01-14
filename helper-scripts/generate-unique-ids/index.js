const fs = require("fs");
const csv = require('csv');
const nanoid = require('nanoid')
const nanoidDictionary = require('nanoid-dictionary')

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

// Set an index to null to omit generation for the associated unique ID
const generateUniqueIds = (language, uniqueIdIndex, cardIdIndex, variationsIndex, variationUniqueIdsIndex) => {
    const inputCSV = `../../csvs/${language}/card.csv`
    const outputCSV = `./temp-${language}-card.csv`

    const readStream = fs.createReadStream(inputCSV)
    const writeStream = fs.createWriteStream(outputCSV)
    const csvStream = csv.parse({ delimiter: "\t" })
    const stringifier = csv.stringify({ delimiter: "\t" });

    const capitalizedLanguage = capitalizeFirstLetter(language)

    const customNanoId = nanoid.customAlphabet(nanoidDictionary.nolookalikesSafe)

    const csvStreamFinished = function () {
        fs.renameSync(outputCSV, inputCSV)
        console.log(`Unique ID generation completed for ${capitalizedLanguage}!`)
    }

    var headerRead = false

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
                data[uniqueIdIndex] = customNanoId()
            } else {
                console.log(`No new unique ID needed for ${capitalizedLanguage} card ${cardID}`)
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
                    var variation = splitVariation[1] + " – " + splitVariation[2]

                    if (splitVariation.length > 3) {
                        variation +=  " – " + splitVariation[3]
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
                    var variation = splitVariation[1] + " – " + splitVariation[2]

                    if (splitVariation.length > 3) {
                        variation +=  " – " + splitVariation[3]
                    }

                    existingVariationUniqueIDs[variation] = variationUniqueId
                })

            // generate unique IDs for variations
            var variationUniqueIds = variations.map(variation => {
                var variationUniqueId = existingVariationUniqueIDs[variation]
                var variationUniqueIdExists = variationUniqueId !== undefined

                if (!variationUniqueIdExists) {
                    console.log(`Generating unique ID for ${capitalizedLanguage} variation ${variation}`)
                    variationUniqueId = customNanoId()
                } else {
                    console.log(`No new unique ID needed for ${capitalizedLanguage} variation ${variation}`)
                }

                return variationUniqueId + " – " + variation
            });

            data[variationUniqueIdsIndex] = variationUniqueIds.join(", ")
        }

        // save CSV row
        stringifier.write(data)
    })
    .on('end', () => {
        csvStreamFinished()
    })
    .on("error", function (error) {
        console.log(error.message)
    })

    stringifier.pipe(writeStream)
    readStream.pipe(csvStream)
}

generateUniqueIds("english", 0, 1, 36, 37)
generateUniqueIds("french", null, null, 14, 15)
generateUniqueIds("german", null, null, 14, 15)
generateUniqueIds("italian", null, null, 14, 15)
generateUniqueIds("spanish", null, null, 14, 15)