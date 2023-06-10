import * as fs from 'fs'
import * as csv from 'csv'
import * as helper from '../helper-functions.js'

// Set an index to null to omit generation for the associated unique ID
export const generateCardPrintingUniqueIds = (language, uniqueIdIndex, cardIdIndex, editionIdIndex, foilingIdIndex, artVariationIndex) => {
    return new Promise((resolve, reject) => {
        const inputCSV = `../../csvs/${language}/card-printing.csv`
        const outputCSV = `./temp-${language}-card-printing.csv`

        const readStream = fs.createReadStream(inputCSV)
        const writeStream = fs.createWriteStream(outputCSV)
        const csvStream = csv.parse({ delimiter: "\t" })
        const stringifier = csv.stringify({ delimiter: "\t" });

        const capitalizedLanguage = helper.capitalizeFirstLetter(language)

        const csvStreamFinished = function (cardPrintingIdsAdded) {
            fs.renameSync(outputCSV, inputCSV)
            console.log(`Unique ID generation completed for ${capitalizedLanguage} card printings with ${cardPrintingIdsAdded} new card printing IDs!`)
        }

        var headerRead = false
        var cardPrintingIdsAdded = 0

        csvStream.on("data", function(data) {
            // Skip header
            if (!headerRead) {
                headerRead = true
                stringifier.write(data)
                return
            }

            // Card Printing Unique ID
            if (
                uniqueIdIndex !== null && uniqueIdIndex !== undefined &&
                cardIdIndex !== null && cardIdIndex !== undefined &&
                editionIdIndex !== null && editionIdIndex !== undefined &&
                foilingIdIndex !== null && foilingIdIndex !== undefined &&
                artVariationIndex !== null && artVariationIndex !== undefined
            ) {
                // current card unique ID data
                var uniqueID = data[uniqueIdIndex]
                var cardID = data[cardIdIndex]
                var edition = data[editionIdIndex]
                var foiling = data[foilingIdIndex]
                var artVariation = data[artVariationIndex]

                var uniqueIdExists = uniqueID.trim() !== ''

                // generate unique ID for card
                if (!uniqueIdExists) {
                    var loggingText = `Generating unique ID for ${capitalizedLanguage} card printing ${cardID} - ${edition} - ${foiling}`

                    if (artVariation.trim() !== '') {
                        loggingText += ` - ${artVariation}`
                    }

                    console.log(loggingText)
                    cardPrintingIdsAdded += 1
                    data[uniqueIdIndex] = helper.customNanoId()
                }
            }

            // save CSV row
            stringifier.write(data)
        })
        .on('end', () => {
            csvStreamFinished(cardPrintingIdsAdded)
            resolve()
        })
        .on("error", function (error) {
            console.log(error.message)
            reject()
        })

        stringifier.pipe(writeStream)
        readStream.pipe(csvStream)
    })
}