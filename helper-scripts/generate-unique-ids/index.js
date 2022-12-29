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

csvStream.on("data", function(data) {
    console.log(data[0].trim() == '' ? 'Generating unique ID for ' + data[1] : 'No new unique ID needed for ' + data[1])
    if (data[0].trim() == '') {
        data[0] = customNanoId()
    }
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
