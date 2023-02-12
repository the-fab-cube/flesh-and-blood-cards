const generators = require('./unique-id-generators')

generators.generateCardUniqueIds("english", 0, 1, 24, 25)
generators.generateCardUniqueIds("french", null, null, 9, 10)
generators.generateCardUniqueIds("german", null, null, 9, 10)
generators.generateCardUniqueIds("italian", null, null, 9, 10)
generators.generateCardUniqueIds("spanish", null, null, 9, 10)

generators.generateSetUniqueIds("english", 0, 1, 3, 4)
generators.generateSetUniqueIds("french", 0, 1, 3, 4)
generators.generateSetUniqueIds("german", 0, 1, 3, 4)
generators.generateSetUniqueIds("italian", 0, 1, 3, 4)
generators.generateSetUniqueIds("spanish", 0, 1, 3, 4)

generators.generateAbilityUniqueIds("english", 0, 1)

generators.generateKeywordUniqueIds("english", 0, 1)

generators.generateTypeUniqueIds("english", 0, 1)

generators.generateLegalityUniqueIds("banned-blitz", 0, 2)
generators.generateLegalityUniqueIds("banned-cc", 0, 2)
generators.generateLegalityUniqueIds("banned-commoner", 0, 2)
generators.generateLegalityUniqueIds("banned-upf", 0, 2)
generators.generateLegalityUniqueIds("living-legend-blitz", 0, 2)
generators.generateLegalityUniqueIds("living-legend-cc", 0, 2)
generators.generateLegalityUniqueIds("suspended-blitz", 0, 2)
generators.generateLegalityUniqueIds("suspended-cc", 0, 2)
generators.generateLegalityUniqueIds("suspended-commoner", 0, 2)