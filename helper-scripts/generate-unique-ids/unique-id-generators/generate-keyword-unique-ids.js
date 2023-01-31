const fs = require("fs");
const csv = require('csv');
const helper = require('../helper-functions')

// Set an index to null to omit generation for the associated unique ID
const generateKeywordUniqueIds = (language, uniqueIdIndex, keywordNameIndex) => {
    const inputCSV = `../../csvs/${language}/keyword.csv`
    const outputCSV = `./temp-${language}-keyword.csv`

    const readStream = fs.createReadStream(inputCSV)
    const writeStream = fs.createWriteStream(outputCSV)
    const csvStream = csv.parse({ delimiter: "\t" })
    const stringifier = csv.stringify({ delimiter: "\t" });

    const capitalizedLanguage = helper.capitalizeFirstLetter(language)

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
                data[uniqueIdIndex] = helper.customNanoId()
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

module.exports = {
    generateKeywordUniqueIds
}