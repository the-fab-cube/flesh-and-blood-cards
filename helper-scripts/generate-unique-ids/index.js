const fs = require("fs");
const csv = require('csv');
const nanoid = require('nanoid')
const nanoidDictionary = require('nanoid-dictionary')
const customNanoId = nanoid.customAlphabet(nanoidDictionary.nolookalikesSafe)

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

// Set an index to null to omit generation for the associated unique ID
const generateCardUniqueIds = (language, uniqueIdIndex, cardIdIndex, variationsIndex, variationUniqueIdsIndex) => {
    const inputCSV = `../../csvs/${language}/card.csv`
    const outputCSV = `./temp-${language}-card.csv`

    const readStream = fs.createReadStream(inputCSV)
    const writeStream = fs.createWriteStream(outputCSV)
    const csvStream = csv.parse({ delimiter: "\t" })
    const stringifier = csv.stringify({ delimiter: "\t" });

    const capitalizedLanguage = capitalizeFirstLetter(language)

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
                data[uniqueIdIndex] = customNanoId()
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
                    variationIdsAdded += 1
                    variationUniqueId = customNanoId()
                } else {
                    // console.log(`No new unique ID needed for ${capitalizedLanguage} variation ${variation}`)
                }

                return variationUniqueId + " – " + variation
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

// Set an index to null to omit generation for the associated unique ID
const generateSetUniqueIds = (language, editionsIndex, editionUniqueIdsIndex) => {
    const inputCSV = `../../csvs/${language}/set.csv`
    const outputCSV = `./temp-${language}-set.csv`

    const readStream = fs.createReadStream(inputCSV)
    const writeStream = fs.createWriteStream(outputCSV)
    const csvStream = csv.parse({ delimiter: "\t" })
    const stringifier = csv.stringify({ delimiter: "\t" });

    const capitalizedLanguage = capitalizeFirstLetter(language)

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
                    editionUniqueId = customNanoId()
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

// Set an index to null to omit generation for the associated unique ID
const generateKeywordUniqueIds = (language, uniqueIdIndex, keywordNameIndex) => {
    const inputCSV = `../../csvs/${language}/keyword.csv`
    const outputCSV = `./temp-${language}-keyword.csv`

    const readStream = fs.createReadStream(inputCSV)
    const writeStream = fs.createWriteStream(outputCSV)
    const csvStream = csv.parse({ delimiter: "\t" })
    const stringifier = csv.stringify({ delimiter: "\t" });

    const capitalizedLanguage = capitalizeFirstLetter(language)

    const csvStreamFinished = function (keywordIdsAdded) {
        fs.renameSync(outputCSV, inputCSV)
        console.log(`Unique ID generation completed for ${capitalizedLanguage} keywords with ${keywordIdsAdded} new keyword IDs!`)
    }

    var headerRead = false
    var keywordIdsAdded = 0

    csvStream.on("data", function(data) {
        // Skip header
        if (!headerRead) {
            headerRead = true
            stringifier.write(data)
            return
        }

        // Keyword Unique ID
        if (uniqueIdIndex !== null && uniqueIdIndex !== undefined && keywordNameIndex !== null && keywordNameIndex !== undefined) {
            // current keyword unique ID data
            var uniqueID = data[uniqueIdIndex]
            var keywordName = data[keywordNameIndex]

            var uniqueIdExists = uniqueID.trim() !== ''

            // generate unique ID for keyword
            if (!uniqueIdExists) {
                console.log(`Generating unique ID for ${capitalizedLanguage} keyword ${keywordName}`)
                keywordIdsAdded += 1
                data[uniqueIdIndex] = customNanoId()
            } else {
                // console.log(`No new unique ID needed for ${capitalizedLanguage} keyword ${keywordName}`)
            }
        }

        // save CSV row
        stringifier.write(data)
    })
    .on('end', () => {
        csvStreamFinished(keywordIdsAdded)
    })
    .on("error", function (error) {
        console.log(error.message)
    })

    stringifier.pipe(writeStream)
    readStream.pipe(csvStream)
}

// Set an index to null to omit generation for the associated unique ID
const generateTypeUniqueIds = (language, uniqueIdIndex, typeNameIndex) => {
    const inputCSV = `../../csvs/${language}/type.csv`
    const outputCSV = `./temp-${language}-type.csv`

    const readStream = fs.createReadStream(inputCSV)
    const writeStream = fs.createWriteStream(outputCSV)
    const csvStream = csv.parse({ delimiter: "\t" })
    const stringifier = csv.stringify({ delimiter: "\t" });

    const capitalizedLanguage = capitalizeFirstLetter(language)

    const csvStreamFinished = function (typeIdsAdded) {
        fs.renameSync(outputCSV, inputCSV)
        console.log(`Unique ID generation completed for ${capitalizedLanguage} types with ${typeIdsAdded} new type IDs!`)
    }

    var headerRead = false
    var typeIdsAdded = 0

    csvStream.on("data", function(data) {
        // Skip header
        if (!headerRead) {
            headerRead = true
            stringifier.write(data)
            return
        }

        // Type Unique ID
        if (uniqueIdIndex !== null && uniqueIdIndex !== undefined && typeNameIndex !== null && typeNameIndex !== undefined) {
            // current type unique ID data
            var uniqueID = data[uniqueIdIndex]
            var typeName = data[typeNameIndex]

            var uniqueIdExists = uniqueID.trim() !== ''

            // generate unique ID for type
            if (!uniqueIdExists) {
                console.log(`Generating unique ID for ${capitalizedLanguage} type ${typeName}`)
                typeIdsAdded += 1
                data[uniqueIdIndex] = customNanoId()
            } else {
                // console.log(`No new unique ID needed for ${capitalizedLanguage} type ${typeName}`)
            }
        }

        // save CSV row
        stringifier.write(data)
    })
    .on('end', () => {
        csvStreamFinished(typeIdsAdded)
    })
    .on("error", function (error) {
        console.log(error.message)
    })

    stringifier.pipe(writeStream)
    readStream.pipe(csvStream)
}

generateCardUniqueIds("english", 0, 1, 36, 37)
generateCardUniqueIds("french", null, null, 14, 15)
generateCardUniqueIds("german", null, null, 14, 15)
generateCardUniqueIds("italian", null, null, 14, 15)
generateCardUniqueIds("spanish", null, null, 14, 15)

generateSetUniqueIds("english", 2, 3)
generateSetUniqueIds("french", 2, 3)
generateSetUniqueIds("german", 2, 3)
generateSetUniqueIds("italian", 2, 3)
generateSetUniqueIds("spanish", 2, 3)

generateKeywordUniqueIds("english", 0, 1)

generateTypeUniqueIds("english", 0, 1)