# Flesh and Blood Cards

## General Overview
This repo is intended as a comprehensive, open-source resource for representing all cards and sets from the Flesh and Blood TCG as CSVs.

Please feel free to clone or fork the repo and generally use it for whatever projects you like. I put this together so the community doesn't have to
keep re-entering the same data! I would absolutely appreciate any contributions if you notice any missing data or mistakes. :)


## Approach to reprints/editions
This repo treats a unique card (name + pitch value) as 1 entity. A unique card can have multiple printings, foils, editions, etc, but is considered 1 entry in the CSVs.

A card's text and other data will always be based off the latest erratas and printings.

Similarly, a set is unique based on a setcode + name, and can have multiple editions, but is considered to be 1 entry within the CSV.

## Contributing
If you would like to contribute, please take a look at the format below to see how various CSV fields should be formatted, and then open a PR for any changes you'd like to make.


## CSV Formats

### Set
| Field Name | Intended Data Type | Explanation | Example |
| --- | --- | --- | --- |
| Identifier | string | The set code. | WTR |
| Name | string | The full name of the set. | Welcome to Rathe |
| Editions | string[] | The list of editions printed. | Alpha, Unlimited |
| Initial Release Date | datetime[] | The release date for the set in ISO 8601 format and UTC timezone, correlated to the Editions field. | 2019-10-11T00:00:00.000Z, 2020-11-06T00:00:00.000Z |
| Product Sites | string[] | The list of urls for fabtcg.com product pages, correlated to the Editions field. | https://fabtcg.com/products/booster-set/welcome-rathe/, https://fabtcg.com/products/booster-set/welcome-rathe-unlimited/ |


### Card
| Field Name | Intended Data Type | Explanation | Example |
| --- | --- | --- | --- |
| Identifiers | string[] | The identifiers for the card's various printings. | WTR110, KSU016, LGS007 |
| Set Identifiers | string[] | The set identifiers for the card's various printings. | WTR, KSU, LGS |
| Name | string | The name of the card. (Do not include pitch here.) | Whelming Gustwave |
| Cost | int \| string \| null | The cost of the card. Either a numerical cost, a text cost for special cases like 'XX', or empty for cards with no cost value (ex: Eye of Ophidia). | 0 |
| Pitch | int \| null | The pitch value of the card. Either a numerical value or empty for cards with no pitch value. | 1 |
| Attack | int \| string \| null | The attack value of the card. Either a numerical value, a text cost for special cases like '*', or empty for cards with no attack. | 3 |
| Defense | int \| string \| null | The defense value of the card. Either a numerical value, a text cost for special cases like '*', or empty for cards with no defense. | 3 |
| Rarity | string[] | The rarities the card has been printed at, correlated to the Identifiers field. (Use rarity shorthand, not full rarity names.) | C, C, P |
| Types | string[] | The types of the card. See below for a list of possible types. | Action, Attack, Ninja |
| Keywords | string[] | Any keywords that appear on the card. See below for a list of possible keywords. (Include conditional keywords.) | Combo, Go again |
| Essences | string[] | A list of any essences the card has (likely if it is an elemental hero). | Ice, Earth |
| Functional Text | string | The functional text that effects gameplay. Use the text from the latest printing or errata. Use [Markdown](https://www.markdownguide.org/basic-syntax/) for bold, italic, etc., and use the list of game icon representations below for representing attack icons, defense icons, etc. | **Combo** - If Surging Strike was the last attack this combat chain, Whelming Gustwave gains +1 {{attack}}, **go again**, and "If this hits, draw a card." |
| Flavor Text | string | Any flavor text that appears on the latest printing of the card with flavor text. Do not use italics on this, text is assumed to be in italics. (Example pulled from Talisman of Warfare.) | It's said that wherever the Dracai of War planted this talisman, the lava was soon to flow. |
| Type Text | string | The type text as printed on the latest edition of the card. | Ninja Action - Attack |
| Card Played Horizontally | bool | Is the card played horizontally (Ex: Landmarks)? No value is considered No. | Yes |
| Blitz Legal | bool | Is the card legal in the Blitz format? No value is considered No. | Yes |
| CC Legal | bool | Is the card legal in the Classic Constructed format? No value is considered No. | Yes |
| Variations | string[] | The list of foilings the card is available in within a set/edition combination, as well as any alternate arts for the card. The [Collector's Center](https://fabtcg.com/collectors-centre/) has good resources for finding details on this. If there is an alternate art, make a separate entry in this array and tack on the shorthand for the alternate art type. Format: `{Foiling Shorthands separated by spaces} - {Card Identifier} - {Set Edition Shorthand} (- {Alternate Art Shorthand})` (Using Channel Lake Frigid in this example.) | S R - ELE146 - F, R - ELE146 - F - AA, S R - ELE146 - U |
| Image URLs | string[] | Links to images from fabtcg.com's [image galleries](https://fabtcg.com/resources/card-galleries/) for a set/edition combination. If there is an alternate art, make a separate entry in this array and tack on the shorthand for the alternate art type. Format: `{Image URL} - {Card Identifier} - {Set Edition Shorthand} (- {Alternate Art Shorthand})` (Using Channel Lake Frigid in this example.) | https://storage.googleapis.com/fabmaster/media/images/ELE146.width-450.png - ELE146 - F, https://product-images.tcgplayer.com/fit-in/400x558/248564.jpg - ELE146 - F - AA, https://storage.googleapis.com/fabmaster/media/images/U-ELE146.width-450.png - ELE146 - U |