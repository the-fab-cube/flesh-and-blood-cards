import * as fs from 'fs'
import * as csv from 'csv'
import * as helper from '../helper-functions.js'

// Set an index to null to omit generation for the associated unique ID
export const generateSetUniqueIds = (language, uniqueIdIndex, setIdIndex, nameIndex) => {
    return new Promise((resolve, reject) => {
        const inputCSV = `../../csvs/${language}/set.csv`
        const outputCSV = `./temp-${language}-set.csv`

        const readStream = fs.createReadStream(inputCSV)
        const writeStream = fs.createWriteStream(outputCSV)
        const csvStream = csv.parse({ delimiter: "\t" })
        const stringifier = csv.stringify({ delimiter: "\t" });

        const capitalizedLanguage = helper.capitalizeFirstLetter(language)

        const csvStreamFinished = function (setIdsAdded) {
            fs.renameSync(outputCSV, inputCSV)
            console.log(`Unique ID generation completed for ${capitalizedLanguage} sets with ${setIdsAdded} new set IDs!`)
        }

        var headerRead = false
        var setIdsAdded = 0

        csvStream.on("data", function(data) {
            // Skip header
            if (!headerRead) {
                headerRead = true
                stringifier.write(data)
                return
            }

            // Set Unique ID
            if (
                uniqueIdIndex !== null && uniqueIdIndex !== undefined &&
                setIdIndex !== null && setIdIndex !== undefined &&
                nameIndex !== null && nameIndex !== undefined
            ) {
                // current set unique ID data
                var uniqueID = data[uniqueIdIndex]
                var setID = data[setIdIndex]
                var name = data[nameIndex]

                var uniqueIdExists = uniqueID.trim() !== ''

                // generate unique ID for set
                if (!uniqueIdExists) {
                    console.log(`Generating unique ID for ${capitalizedLanguage} set ${setID} - ${name}`)
                    setIdsAdded += 1
                    data[uniqueIdIndex] = helper.customNanoId()
                } else {
                    // console.log(`No new unique ID needed for ${capitalizedLanguage} set ${cardID}`)
                }
            }

            // save CSV row
            stringifier.write(data)
        })
        .on('end', () => {
            csvStreamFinished(setIdsAdded)
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