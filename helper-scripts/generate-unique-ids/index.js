import * as generators from './unique-id-generators/index.js'


// TODO: Fix
// generators.generateCardUniqueIds("french", null, null, 9, 10)
// generators.generateCardUniqueIds("german", null, null, 9, 10)
// generators.generateCardUniqueIds("italian", null, null, 9, 10)
// generators.generateCardUniqueIds("spanish", null, null, 9, 10)

// TODO: Add card printing unique id generator for non-english cards

// Setup a loop to wait for all generators to be finished
var timeout

const waitForPromisesToFinishLoop = () => {
    timeout = setTimeout(() => { waitForPromisesToFinishLoop() }, 1 * 1000)
}

const promisesFinished = () => {
    clearTimeout(timeout)
}

waitForPromisesToFinishLoop()

// Kick-off all generators

await Promise.allSettled([
    generators.generateCardUniqueIds("english", 0, 1, 2),

    generators.generateCardPrintingUniqueIds("english", 0, 4, 7, 9, 10),

    generators.generateSetUniqueIds("english", 0, 1, 3, 4),
    generators.generateSetUniqueIds("french", 0, 1, 3, 4),
    generators.generateSetUniqueIds("german", 0, 1, 3, 4),
    generators.generateSetUniqueIds("italian", 0, 1, 3, 4),
    generators.generateSetUniqueIds("spanish", 0, 1, 3, 4),

    generators.generateAbilityUniqueIds("english", 0, 1),

    generators.generateKeywordUniqueIds("english", 0, 1),

    generators.generateTypeUniqueIds("english", 0, 1),

    generators.generateLegalityUniqueIds("banned-blitz", 0, 2),
    generators.generateLegalityUniqueIds("banned-cc", 0, 2),
    generators.generateLegalityUniqueIds("banned-commoner", 0, 2),
    generators.generateLegalityUniqueIds("banned-upf", 0, 2),
    generators.generateLegalityUniqueIds("living-legend-blitz", 0, 2),
    generators.generateLegalityUniqueIds("living-legend-cc", 0, 2),
    generators.generateLegalityUniqueIds("suspended-blitz", 0, 2),
    generators.generateLegalityUniqueIds("suspended-cc", 0, 2),
    generators.generateLegalityUniqueIds("suspended-commoner", 0, 2)
]).then(() => promisesFinished())

