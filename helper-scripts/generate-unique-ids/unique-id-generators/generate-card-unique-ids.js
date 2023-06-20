import * as fs from 'fs'
import * as csv from 'csv'
import * as helper from '../helper-functions.js'

// Set an index to null to omit generation for the associated unique ID
export const generateCardUniqueIds = (language, uniqueIdIndex, nameIdIndex, pitchIdIndex) => {
    return new Promise((resolve, reject) => {
        const inputCSV = `../../csvs/${language}/card.csv`
        const outputCSV = `./temp-${language}-card.csv`

        const readStream = fs.createReadStream(inputCSV)
        const writeStream = fs.createWriteStream(outputCSV)
        const csvStream = csv.parse({ delimiter: "\t" })
        const stringifier = csv.stringify({ delimiter: "\t" });

        const capitalizedLanguage = helper.capitalizeFirstLetter(language)

        const csvStreamFinished = function (cardIdsAdded) {
            fs.renameSync(outputCSV, inputCSV)
            console.log(`Unique ID generation completed for ${capitalizedLanguage} cards with ${cardIdsAdded} new card IDs!`)
        }

        var headerRead = false
        var cardIdsAdded = 0

        csvStream.on("data", function(data) {
            // Skip header
            if (!headerRead) {
                headerRead = true
                stringifier.write(data)
                return
            }

            // Card Unique ID
            if (
                uniqueIdIndex !== null && uniqueIdIndex !== undefined &&
                nameIdIndex !== null && nameIdIndex !== undefined &&
                pitchIdIndex !== null && pitchIdIndex !== undefined
            ) {
                // current card unique ID data
                var uniqueID = data[uniqueIdIndex]
                var name = data[nameIdIndex]
                var pitch = data[pitchIdIndex]

                var uniqueIdExists = uniqueID.trim() !== ''

                // generate unique ID for card
                if (!uniqueIdExists) {
                    var loggingText = `Generating unique ID for ${capitalizedLanguage} card ${name}`

                    if (pitch.trim() !== '') {
                        loggingText += ` - ${pitch}`
                    }

                    console.log(loggingText)
                    cardIdsAdded += 1
                    data[uniqueIdIndex] = helper.customNanoId()
                }
            }

            // save CSV row
            stringifier.write(data)
        })
        .on('end', () => {
            csvStreamFinished(cardIdsAdded)
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