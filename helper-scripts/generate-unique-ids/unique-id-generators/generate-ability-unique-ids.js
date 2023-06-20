import * as fs from 'fs'
import * as csv from 'csv'
import * as helper from '../helper-functions.js'

// Set an index to null to omit generation for the associated unique ID
export const generateAbilityUniqueIds = (language, uniqueIdIndex, abilityNameIndex) => {
    return new Promise((resolve, reject) => {
        const inputCSV = `../../csvs/${language}/ability.csv`
        const outputCSV = `./temp-${language}-ability.csv`

        const readStream = fs.createReadStream(inputCSV)
        const writeStream = fs.createWriteStream(outputCSV)
        const csvStream = csv.parse({ delimiter: "\t" })
        const stringifier = csv.stringify({ delimiter: "\t" });

        const capitalizedLanguage = helper.capitalizeFirstLetter(language)

        const csvStreamFinished = function (abilityIdsAdded) {
            fs.renameSync(outputCSV, inputCSV)
            console.log(`Unique ID generation completed for ${capitalizedLanguage} abilities with ${abilityIdsAdded} new ability IDs!`)
        }

        var headerRead = false
        var abilityIdsAdded = 0

        csvStream.on("data", function(data) {
            // Skip header
            if (!headerRead) {
                headerRead = true
                stringifier.write(data)
                return
            }

            // Ability Unique ID
            if (uniqueIdIndex !== null && uniqueIdIndex !== undefined && abilityNameIndex !== null && abilityNameIndex !== undefined) {
                // current ability unique ID data
                var uniqueID = data[uniqueIdIndex]
                var abilityName = data[abilityNameIndex]

                var uniqueIdExists = uniqueID.trim() !== ''

                // generate unique ID for ability
                if (!uniqueIdExists) {
                    console.log(`Generating unique ID for ${capitalizedLanguage} ability ${abilityName}`)
                    abilityIdsAdded += 1
                    data[uniqueIdIndex] = helper.customNanoId()
                } else {
                    // console.log(`No new unique ID needed for ${capitalizedLanguage} ability ${abilityName}`)
                }
            }

            // save CSV row
            stringifier.write(data)
        })
        .on('end', () => {
            csvStreamFinished(abilityIdsAdded)
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