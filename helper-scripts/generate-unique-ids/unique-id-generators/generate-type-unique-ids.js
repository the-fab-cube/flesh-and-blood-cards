import * as fs from 'fs'
import * as csv from 'csv'
import * as helper from '../helper-functions.js'

// Set an index to null to omit generation for the associated unique ID
export const generateTypeUniqueIds = (language, uniqueIdIndex, typeNameIndex) => {
    return new Promise((resolve, reject) => {
        const inputCSV = `../../csvs/${language}/type.csv`
        const outputCSV = `./temp-${language}-type.csv`

        const readStream = fs.createReadStream(inputCSV)
        const writeStream = fs.createWriteStream(outputCSV)
        const csvStream = csv.parse({ delimiter: "\t" })
        const stringifier = csv.stringify({ delimiter: "\t" });

        const capitalizedLanguage = helper.capitalizeFirstLetter(language)

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
                    data[uniqueIdIndex] = helper.customNanoId()
                } else {
                    // console.log(`No new unique ID needed for ${capitalizedLanguage} type ${typeName}`)
                }
            }

            // save CSV row
            stringifier.write(data)
        })
        .on('end', () => {
            csvStreamFinished(typeIdsAdded)
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