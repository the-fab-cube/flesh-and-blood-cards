const generators = require('./unique-id-generators')

generators.generateCardUniqueIds("english", 0, 1, 36, 37)
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
