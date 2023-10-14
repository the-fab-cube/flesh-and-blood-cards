import * as fs from 'fs'
import * as csv from 'csv'
import * as helper from './helper-functions.js'

// Set an index to null to omit generation for the associated unique ID
export const populateProductIds = (productDetails, language, setIdToMatch, cardIdIndex, rarityIndex, artVariationIndex, productIdIndex) => {
    return new Promise((resolve, reject) => {
        const inputCSV = `../../csvs/${language}/card-printing.csv`
        const outputCSV = `./temp-${language}-card-printing.csv`

        const readStream = fs.createReadStream(inputCSV)
        const writeStream = fs.createWriteStream(outputCSV)
        const csvStream = csv.parse({ delimiter: "\t" })
        const stringifier = csv.stringify({ delimiter: "\t" });

        const capitalizedLanguage = helper.capitalizeFirstLetter(language)

        const csvStreamFinished = function (cardPrintingIdsAdded) {
            fs.renameSync(outputCSV, inputCSV)
            console.log(`Product ID population completed for ${capitalizedLanguage} ${setIdToMatch} card printings with ${cardPrintingIdsAdded} new product IDs!`)
        }

        var headerRead = false
        var cardPrintingIdsAdded = 0

        csvStream.on("data", function(data) {
            // Skip header
            if (!headerRead) {
                headerRead = true
                stringifier.write(data)
                return
            }

            // Card Printing Unique ID
            if (
                cardIdIndex !== null && cardIdIndex !== undefined &&
                rarityIndex !== null && rarityIndex !== undefined &&
                artVariationIndex !== null && artVariationIndex !== undefined &&
                productIdIndex !== null && productIdIndex !== undefined
            ) {
                // current card unique ID data
                var cardId = data[cardIdIndex]
                var rarity = data[rarityIndex]
                var artVariation = data[artVariationIndex]
                var productId = data[productIdIndex]

                var productIdExists = productId.trim() !== ''

                // generate unique ID for card
                if (!productIdExists && cardId.includes(setIdToMatch)) {
                    const matchingProductDetail = findMatchingProductDetail(productDetails, cardId, rarity, artVariation)

                    if (matchingProductDetail) {
                        data[productIdIndex] = matchingProductDetail.productId
                        cardPrintingIdsAdded += 1
                    }
                }
            }

            // save CSV row
            stringifier.write(data)
        })
        .on('end', () => {
            csvStreamFinished(cardPrintingIdsAdded)
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

const findMatchingProductDetail = (productDetails, cardId, rarity, artVariation) => {
    const matchingDetails = productDetails.filter(productDetail => productDetail.cardId == cardId && productDetail.rarity == rarity)

    if (matchingDetails.length != 1) {
        const matchingExtendedArtDetails = matchingDetails.filter(productDetail => productDetail.name.toLowerCase().includes("extended art"))
        const matchingNonExtendedArtDetails = matchingDetails.filter(productDetail => !productDetail.name.toLowerCase().includes("extended art"))

        if (!artVariation && matchingNonExtendedArtDetails.length == 1) {
            return matchingNonExtendedArtDetails[0]
        }

        if (artVariation == 'EA' && matchingExtendedArtDetails.length == 1) {
            return matchingExtendedArtDetails[0]
        }

        console.log(`Could not properly match product ID for ${cardId} - found ${matchingDetails.length} matches!`)
        return null
    }

    return matchingDetails[0]
}