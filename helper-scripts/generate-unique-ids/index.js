const fs = require("fs");
const csv = require('csv');
const nanoid = require('nanoid')
const nanoidDictionary = require('nanoid-dictionary')

const inputCSV = "../../csvs/english/card.csv"
const outputCSV = "./temp-card.csv"

const readStream = fs.createReadStream(inputCSV)
const writeStream = fs.createWriteStream(outputCSV)
const csvStream = csv.parse({ delimiter: "\t" })
const stringifier = csv.stringify({ delimiter: "\t" });

const customNanoId = nanoid.customAlphabet(nanoidDictionary.nolookalikesSafe)

const csvStreamFinished = function () {
    fs.renameSync(outputCSV, inputCSV)
    console.log('Unique ID generation completed!')
}

var headerRead = false

csvStream.on("data", function(data) {
    // Skip header
    if (!headerRead) {
        headerRead = true
        stringifier.write(data)
        return
    }

    // CSV indexes
    let uniqueIdIndex = 0
    let cardIdIndex = 1
    let variationsIndex = 36
    let variationUniqueIdsIndex = 37

    // curren card unique ID data
    var uniqueID = data[uniqueIdIndex]
    var cardID = data[cardIdIndex]

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

    var uniqueIdExists = uniqueID.trim() !== ''

    // generate unique ID for card
    if (!uniqueIdExists) {
        console.log('Generating unique ID for card ' + cardID)
        data[uniqueIdIndex] = customNanoId()
    } else {
        console.log('No new unique ID needed for card ' + cardID)
    }

    // generate unique IDs for variations
    var variationUniqueIds = variations.map(variation => {
        var variationUniqueId = existingVariationUniqueIDs[variation]
        var variationUniqueIdExists = variationUniqueId !== undefined

        if (!variationUniqueIdExists) {
            console.log('Generating unique ID for variation ' + variation)
            variationUniqueId = customNanoId()
        } else {
            console.log('No new unique ID needed for variation ' + variation)
        }

        return variationUniqueId + " – " + variation
    });

    data[variationUniqueIdsIndex] = variationUniqueIds.join(", ")

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
