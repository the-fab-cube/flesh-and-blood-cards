import * as fs from 'fs'
import * as csv from 'csv'
import * as helper from '../helper-functions.js'

// Set an index to null to omit generation for the associated unique ID
export const generateLegalityUniqueIds = (filename, uniqueIdIndex, cardNameIndex) => {
    return new Promise((resolve, reject) => {
        const inputCSV = `../../csvs/english/${filename}.csv`
        const outputCSV = `./temp-english-${filename}.csv`

        const readStream = fs.createReadStream(inputCSV)
        const writeStream = fs.createWriteStream(outputCSV)
        const csvStream = csv.parse({ delimiter: "\t" })
        const stringifier = csv.stringify({ delimiter: "\t" });

        const csvStreamFinished = function (legalityIdsAdded) {
            fs.renameSync(outputCSV, inputCSV)
            console.log(`Unique ID generation completed for English ${filename} legality file with ${legalityIdsAdded} new IDs!`)
        }

        var headerRead = false
        var legalityIdsAdded = 0

        csvStream.on("data", function(data) {
            // Skip header
            if (!headerRead) {
                headerRead = true
                stringifier.write(data)
                return
            }

            // Type Unique ID
            if (uniqueIdIndex !== null && uniqueIdIndex !== undefined && cardNameIndex !== null && cardNameIndex !== undefined) {
                // current type unique ID data
                var uniqueID = data[uniqueIdIndex]
                var cardName = data[cardNameIndex]

                var uniqueIdExists = uniqueID.trim() !== ''

                // generate unique ID for type
                if (!uniqueIdExists) {
                    console.log(`Generating unique ID for English ${filename} ${cardName} legality info`)
                    legalityIdsAdded += 1
                    data[uniqueIdIndex] = helper.customNanoId()
                } else {
                    // console.log(`No new unique ID needed for English type ${cardName} legality`)
                }
            }

            // save CSV row
            stringifier.write(data)
        })
        .on('end', () => {
            csvStreamFinished(legalityIdsAdded)
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