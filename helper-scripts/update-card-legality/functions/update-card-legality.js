import * as fs from 'fs'
import * as csv from 'csv'

const specialUsePromos = [
    "Adaptive Cadaver",
    "Brush of Heavenly Rites",
    "Cracker Bauble",
    "Cut to Shreds",
    "Death's Door Knocker",
    "Diamond Hands",
    "Fabric of Blossoms",
    "Fabric of Hope",
    "Fabric of Providence",
    "Fabric of Scales",
    "Fabric of Spring",
    "Frankie, Make Ends Meat",
    "Gavel of Natural Order",
    "Go Bananas",
    "Good Deeds Don't Go Unnoticed",
    "Hemlock Heels",
    "Hummingbird, Call of Adventure",
    "Intellect Penalty",
    "Magrar",
    "Morbid Shears",
    "Off Cuts",
    "Pink Visor",
    "Popped Collar Polo",
    "Proclamation of Abundance",
    "Proclamation of Combat",
    "Proclamation of Production",
    "Proclamation of Requisition",
    "Scarf for a Scarf",
    "Shitty Xmas Present",
    "Silversheen Needle",
    "Skull Candy",
    "Spirit of Christmas",
    "Squizzy & Floof",
    "Sugar Casket",
    "Tales of Adventure",
    "Taylor",
    "Venomback Fabric",
    "Yorick, Weaver of Tales",
]

// Set an index to null to omit generation for the associated unique ID
export const updateCardLegality = (printingDictionary) => {
    return new Promise((resolve, reject) => {
        const inputCSV = `../../csvs/english/card.csv`
        const outputCSV = `./temp-english-card.csv`

        const readStream = fs.createReadStream(inputCSV)
        const writeStream = fs.createWriteStream(outputCSV)
        const csvStream = csv.parse({ delimiter: "\t" })
        const stringifier = csv.stringify({ delimiter: "\t" });

        // Get printings

        const csvStreamFinished = function (blitzLegalityUpdatedCount, ccLegalityUpdatedCount, commonerLegalityUpdatedCount, livingLegendLegalityUpdatedCount, silverAgeLegalityUpdatedCount) {
            fs.renameSync(outputCSV, inputCSV)
            console.log("")
            console.log(`Blitz legality updated for ${blitzLegalityUpdatedCount} cards!`)
            console.log(`CC legality updated for ${ccLegalityUpdatedCount} cards!`)
            console.log(`Commoner legality updated for ${commonerLegalityUpdatedCount} cards!`)
            console.log(`Living Legend legality updated for ${livingLegendLegalityUpdatedCount} cards!`)
            console.log(`Silver Age legality updated for ${silverAgeLegalityUpdatedCount} cards!`)
        }

        var headerRead = false
        var blitzLegalityUpdatedCount = 0
        var ccLegalityUpdatedCount = 0
        var commonerLegalityUpdatedCount = 0
        var llLegalityUpdatedCount = 0
        var silverAgeLegalityUpdatedCount = 0

        var uniqueIdIndex = 0
        var nameIdIndex = 1
        var pitchIdIndex = 3
        var typesIndex = 10
        var blitzLegalityIndex = 21
        var ccLegalityIndex = 22
        var silverAgeLegalityIndex = 23
        var commonerLegalityIndex = 24
        var llLegalityIndex = 25

        csvStream.on("data", function(data) {
            // Skip header
            if (!headerRead) {
                headerRead = true
                stringifier.write(data)
                return
            }

            // Card Unique ID

            // current card data
            var uniqueId = data[uniqueIdIndex]
            var name = data[nameIdIndex]
            var pitch = data[pitchIdIndex]
            var types = data[typesIndex].split(", ")

            // Blitz

            var currentBlitzLegality = parseCsvLegality(data[blitzLegalityIndex])
            var calculatedBlitzLegality = calculateBlitzLegality(name, types)

            if (currentBlitzLegality != calculatedBlitzLegality) {
                var loggingText = `Updating Blitz legality for card ${name}`

                if (pitch.trim() !== '') {
                    loggingText += ` - ${pitch}`
                }

                console.log(loggingText)
                blitzLegalityUpdatedCount += 1

                data[blitzLegalityIndex] = convertToCsvLegality(calculatedBlitzLegality)
            }

            // CC

            var currentCcLegality = parseCsvLegality(data[ccLegalityIndex])
            var calculatedCcLegality = calculateCcLegality(name, types)

            if (currentCcLegality != calculatedCcLegality) {
                var loggingText = `Updating CC legality for card ${name}`

                if (pitch.trim() !== '') {
                    loggingText += ` - ${pitch}`
                }

                console.log(loggingText)
                ccLegalityUpdatedCount += 1

                data[ccLegalityIndex] = convertToCsvLegality(calculatedCcLegality)
            }

            // Commoner

            var currentCommonerLegality = parseCsvLegality(data[commonerLegalityIndex])
            var calculatedCommonerLegality = calculateCommonerLegality(uniqueId, name, types, printingDictionary)

            if (currentCommonerLegality != calculatedCommonerLegality) {
                var loggingText = `Updating Commoner legality for card ${name}`

                if (pitch.trim() !== '') {
                    loggingText += ` - ${pitch}`
                }

                console.log(loggingText)
                commonerLegalityUpdatedCount += 1

                data[commonerLegalityIndex] = convertToCsvLegality(calculatedCommonerLegality)
            }

            // Living Legend

            var currentLlLegality = parseCsvLegality(data[llLegalityIndex])
            var calculatedLlLegality = calculateLlLegality(name, types)

            if (currentLlLegality != calculatedLlLegality) {
                var loggingText = `Updating LL legality for card ${name}`

                if (pitch.trim() !== '') {
                    loggingText += ` - ${pitch}`
                }

                console.log(loggingText)
                llLegalityUpdatedCount += 1

                data[llLegalityIndex] = convertToCsvLegality(calculatedLlLegality)
            }

            // Silver Age

            var currentSilverAgeLegality = parseCsvLegality(data[silverAgeLegalityIndex])
            var calculatedSilverAgeLegality = calculateSilverAgeLegality(uniqueId, name, types, printingDictionary)

            if (currentSilverAgeLegality != calculatedSilverAgeLegality) {
                var loggingText = `Updating Silver Age legality for card ${name}`

                if (pitch.trim() !== '') {
                    loggingText += ` - ${pitch}`
                }

                console.log(loggingText)
                silverAgeLegalityUpdatedCount += 1

                data[silverAgeLegalityIndex] = convertToCsvLegality(calculatedSilverAgeLegality)
            }

            // save CSV row
            stringifier.write(data)
        })
        .on('end', () => {
            csvStreamFinished(blitzLegalityUpdatedCount, ccLegalityUpdatedCount, commonerLegalityUpdatedCount, llLegalityUpdatedCount, silverAgeLegalityUpdatedCount)
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

// Parse CSV

function parseCsvLegality(value) {
    return value == "No" ? false : true
}

function convertToCsvLegality(value) {
    return value ? "" : "No"
}

// Calculate Legality

function calculateBlitzLegality(name, types) {
    if (
        (types.includes("Hero") && !types.includes("Young")) ||
        types.includes("Event") ||
        types.includes("Pit-Fighter") ||
        specialUsePromos.includes(name)
    ) {
        return false
    }

    return true
}

function calculateCcLegality(name, types) {
    if (
        (types.includes("Hero") && types.includes("Young")) ||
        types.includes("Event") ||
        types.includes("Mentor") ||
        types.includes("Pit-Fighter") ||
        specialUsePromos.includes(name)
    ) {
        return false
    }

    return true
}

function calculateCommonerLegality(uniqueId, name, types, printingDictionary) {
    if (
        (types.includes("Hero") && !types.includes("Young")) ||
        types.includes("Event") ||
        types.includes("Pit-Fighter") ||
        specialUsePromos.includes(name)
    ) {
        return false
    }

    var printings = printingDictionary[uniqueId]
    
    if (!printings) {
        return false
    }
    
    var cardIsLegal = printings.reduce((previousValue, currentValue) => {
        var printingLegal = currentValue.rarity == 'C' ||
            currentValue.rarity == 'B' ||
            currentValue.rarity == 'T' ||
            (
                currentValue.rarity == 'R' &&
                (
                    types.includes("Hero") ||
                    (
                        (types.includes("Equipment") || types.includes("Weapon")) &&
                        !(types.includes("Action") || types.includes("Instant"))
                    )
                )
            )

        return previousValue || printingLegal
    }, false)

    return cardIsLegal
}

function calculateLlLegality(name, types) {
    if (
        (types.includes("Hero") && types.includes("Young")) ||
        types.includes("Event") ||
        types.includes("Mentor") ||
        types.includes("Pit-Fighter") ||
        specialUsePromos.includes(name)
    ) {
        return false
    }

    return true
}

function calculateSilverAgeLegality(uniqueId, name, types, printingDictionary) {
    if (
        (types.includes("Hero") && !types.includes("Young")) ||
        types.includes("Event") ||
        types.includes("Pit-Fighter") ||
        specialUsePromos.includes(name)
    ) {
        return false
    }

    var printings = printingDictionary[uniqueId]
    
    if (!printings) {
        return false
    }
    
    var cardIsLegal = printings.reduce((previousValue, currentValue) => {
        var printingLegal = currentValue.rarity == 'C' ||
            currentValue.rarity == 'B' ||
            currentValue.rarity == 'T' ||
            currentValue.rarity == 'R' ||
			currentValue.rarity == 'S'

        return previousValue || printingLegal
    }, false)

    return cardIsLegal
}
