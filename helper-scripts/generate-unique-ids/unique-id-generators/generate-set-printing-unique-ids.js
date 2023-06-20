import * as fs from 'fs'
import * as csv from 'csv'
import * as helper from '../helper-functions.js'

// Set an index to null to omit generation for the associated unique ID
export const generateSetPrintingUniqueIds = (language, uniqueIdIndex, startCardIdIndex, editionIndex) => {
    return new Promise((resolve, reject) => {
        const inputCSV = `../../csvs/${language}/set-printing.csv`
        const outputCSV = `./temp-${language}-set-printing.csv`

        const readStream = fs.createReadStream(inputCSV)
        const writeStream = fs.createWriteStream(outputCSV)
        const csvStream = csv.parse({ delimiter: "\t" })
        const stringifier = csv.stringify({ delimiter: "\t" });

        const capitalizedLanguage = helper.capitalizeFirstLetter(language)

        const csvStreamFinished = function (printingIdsAdded) {
            fs.renameSync(outputCSV, inputCSV)
            console.log(`Unique ID generation completed for ${capitalizedLanguage} set printings with ${printingIdsAdded} new set printing IDs!`)
        }

        var headerRead = false
        var printingIdsAdded = 0

        csvStream.on("data", function(data) {
            // Skip header
            if (!headerRead) {
                headerRead = true
                stringifier.write(data)
                return
            }

            // Set Printing Unique ID
            if (
                uniqueIdIndex !== null && uniqueIdIndex !== undefined &&
                startCardIdIndex !== null && startCardIdIndex !== undefined &&
                editionIndex !== null && editionIndex !== undefined
            ) {
                // current set printing unique ID data
                var uniqueId = data[uniqueIdIndex]
                var startCardId = data[startCardIdIndex]
                var edition = data[editionIndex]
                var setId = startCardId.substring(0, 3)

                var uniqueIdExists = uniqueId.trim() !== ''

                // generate unique ID for set printing
                if (!uniqueIdExists) {
                    console.log(`Generating unique ID for ${capitalizedLanguage} set printing ${setId} - ${edition}`)
                    printingIdsAdded += 1
                    data[uniqueIdIndex] = helper.customNanoId()
                } else {
                    // console.log(`No new unique ID needed for ${capitalizedLanguage} set printing ${cardID}`)
                }
            }

            // save CSV row
            stringifier.write(data)
        })
        .on('end', () => {
            csvStreamFinished(printingIdsAdded)
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