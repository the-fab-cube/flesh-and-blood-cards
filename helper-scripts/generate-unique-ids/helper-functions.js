const nanoid = require('nanoid')
const nanoidDictionary = require('nanoid-dictionary')
const customNanoId = nanoid.customAlphabet(nanoidDictionary.nolookalikesSafe)

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

module.exports = {
    customNanoId,
    capitalizeFirstLetter
}