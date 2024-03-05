import * as generators from './unique-id-generators/index.js'

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
    generators.generateCardPrintingUniqueIds("french", 0, 4, 7, 9, 10),
    generators.generateCardPrintingUniqueIds("german", 0, 4, 7, 9, 10),
    generators.generateCardPrintingUniqueIds("italian", 0, 4, 7, 9, 10),
    generators.generateCardPrintingUniqueIds("spanish", 0, 4, 7, 9, 10),

    generators.generateSetUniqueIds("english", 0, 1, 2),

    generators.generateSetPrintingUniqueIds("english", 0, 3, 2),
    generators.generateSetPrintingUniqueIds("french", 0, 1, 3, 4),
    generators.generateSetPrintingUniqueIds("german", 0, 1, 3, 4),
    generators.generateSetPrintingUniqueIds("italian", 0, 1, 3, 4),
    generators.generateSetPrintingUniqueIds("spanish", 0, 1, 3, 4),

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
    generators.generateLegalityUniqueIds("suspended-commoner", 0, 2),
    generators.generateLegalityUniqueIds("restricted-ll", 0, 2)
]).then(() => promisesFinished())

