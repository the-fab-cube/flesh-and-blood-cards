# Flesh and Blood Cards

## General Overview
This repo is intended as a comprehensive, open-source resource for representing all cards and sets from the Flesh and Blood TCG as CSVs.

The CSVs are tab delimited and use " as string indicators.

Please feel free to clone or fork the repo and generally use it for whatever projects you like. I put this together so the community doesn't have to
keep re-entering the same data! I would absolutely appreciate any contributions if you notice any missing data or mistakes. :)

You can view the current CSVs through the web [here](https://the-fab-cube.github.io/flesh-and-blood-cards/).


## Approach to reprints/editions
This repo treats a unique card (name + pitch value) as 1 entity. A unique card can have multiple printings, foils, editions, etc, but is considered 1 entry in the CSVs.

A card's text and other data will always be based off the latest erratas and printings.

Similarly, a set is unique based on a setcode + name, and can have multiple editions, but is considered to be 1 entry within the CSV.


## Contributing
If you would like to contribute, please take a look at the format below to see how various CSV fields should be formatted, and then open a PR for any changes you'd like to make.

The list of open milestones that have card data that needs entering can be found [here](https://github.com/flesh-cube/flesh-and-blood-cards/milestones)

I have LibreOffice files in the repo for easy editing in open-office. It is okay if you do not use them, I will update them with any changes other people make without using LibreOffice,
but they are there for convenience. To use them, just open the .ods file and edit, and then when done, export the file as a .csv to the csvs folder with Save As, making sure to
choose Tabs as the delimiter and " as the string indicator.

## Current Status on CSV Representation of Translated Cards
If you are interested in helping transcribe the History Pack 1 Black Label cards, please comment [here](https://github.com/the-fab-cube/flesh-and-blood-cards/issues/118) to register your interest and I'll get in touch with you when efforts are ready to begin!


## Generate HTML Viewable CSVs

### Install csvtotable
`pyenv install`

`pyenv exec pip install --upgrade csvtotable`

### Serve a specific file
`pyenv exec csvtotable {file}.csv --serve -d $'\t' -q $'"`

### Generate all HTMLs
`./generate-htmls.sh`

## Auto incrementing Image URL values in OpenOffice
1. Go to cell you want to copy URLs of (in our case, Image URLs, which is U8 for us)
2. In an empty column in the same row (in our case, V8), add the card number (for us, 6, since we're starting on WTR6)
3. Go to the next empty column in the same row (in our case, W8), and copy\paste this formula in
    ```=SUBSTITUTE(SUBSTITUTE(SUBSTITUTE($X$8,"WTR006",CONCATENATE("WTR", TEXT(Y8, "000"))),"WTR6",CONCATENATE("WTR", Y8)),"WTR_6",CONCATENATE("WTR_", Y8))```
4. Replace the WTR006, WTR6, WTR_6 values in the formula with the set number you're trying to increment, and replace the instances of $U$8 and V8 with your cell values
5. Drag copy the cells - you should see your formula cell have the proper URLs!
6. Highlight and copy the new cells from the column you generated with formulas
7. Highlight the actual cells you want the URLs in (since they're all copies of the original URL right now)
8. Right click, select Paste Special > Paste Special..., and click Values Only
9. Delete your temporary columns, and you're done!
10. Note: You can use something like this for Variations: `SUBSTITUTE($W$8,"WTR006",CONCATENATE("WTR", TEXT(Y8, "000")))`


## CSV Formats

### Set
| Field Name | Intended Data Type | Explanation | Example |
| --- | --- | --- | --- |
| Identifier | string | The set code. | WTR |
| Name | string | The full name of the set. | Welcome to Rathe |
| Editions | string[] | The list of editions printed. | Alpha, Unlimited |
| Initial Release Dates | datetime[] | The initial release date for the set in ISO 8601 format and UTC timezone, correlated to the Editions field. | 2019-10-11T00:00:00.000Z, 2020-11-06T00:00:00.000Z |
| Out of Print Dates | datetime[] | The Out of Print (OOP) announcement date for the set in ISO 8601 format and UTC timezone, correlated to the Editions field. If the set is still in print, use `null` instead of a date. | 2019-10-11T00:00:00.000Z, 2021-12-01T00:00:00.000Z |
| Start Card Id | string | The id of the first card in the set. | WTR000 |
| End Card Id | string | The id of the first card in the set. | WTR225 |
| Product Pages | string[] | The list of urls for fabtcg.com product pages, correlated to the Editions field. | https://fabtcg.com/products/booster-set/welcome-rathe/, https://fabtcg.com/products/booster-set/welcome-rathe-unlimited/ |
| Collector's Center | string[] | The list of urls for fabtcg.com collector's center pages, correlated to the Editions field. | https://fabtcg.com/collectors-centre/welcome-rathe/, https://fabtcg.com/collectors-centre/welcome-rathe/ |
| Card Galleries | string[] | The list of urls for fabtcg.com card gallery pages, correlated to the Editions field. | https://fabtcg.com/resources/card-galleries/welcome-rathe-booster/, https://fabtcg.com/resources/card-galleries/welcome-rathe-unlimited-booster/ |



### Card
| Field Name | Intended Data Type | Explanation | Example |
| --- | --- | --- | --- |
| Identifiers | string[] | The identifiers for the card's various printings. Order them in this order: set (order of release), non-set (order of release), promo (alphabetically). | WTR110, KSU016, LGS007 |
| Set Identifiers | string[] | The set identifiers for the card's various printings. Order them in this order: set (order of release), non-set (order of release), promo (alphabetically). | WTR, KSU, LGS |
| Name | string | The name of the card. (Do not include pitch here.) | Whelming Gustwave |
| Pitch | int \| null | The pitch value of the card. Either a numerical value or empty for cards with no pitch value. | 1 |
| Cost | int \| string \| null | The cost of the card. Either a numerical cost, a text cost for special cases like 'XX', or empty for cards with no cost value (ex: Eye of Ophidia). | 0 |
| Power | int \| string \| null | The power value of the card. Either a numerical value, a text cost for special cases like '*', or empty for cards with no power. | 3 |
| Defense | int \| string \| null | The defense value of the card. Either a numerical value, a text cost for special cases like '*', or empty for cards with no defense. | 3 |
| Health | int \| null | The health of the (hero) card. Either a numerical value or empty for cards with no health. | 40 |
| Intelligence | int \| null | The intelligence of the (hero) card. Either a numerical value or empty for cards with no intelligence. | 4 |
| Rarities | string[] | The rarities the card has been printed at, correlated to the Identifiers field. (Use rarity shorthand, not full rarity names.) If a rarity was changed mid printing (ex: Zen State went from Rare to Common between CRU First Edition and CRU Unlimited Edition), instead use the format ``{Rarity Shorthand separated by spaces} - {Card Identifier} - {Set Edition Shorthand}` for all rarities. | C, C, P |
| Types | string[] | The types of the card (main type, sub type, talent, etc). See below for a list of possible types. | Action, Attack, Ninja |
| Card Keywords | string[] | Any keywords that appear on the card's effect. See below for a list of possible keywords. (Include keywords that are conditionally granted to the card, but not keywords the card grants or removes from other cards, or keywords on the card's abilities or effect's.) | Combo, Go again |
| Abilities and Effects | string[] | A list of any types of abilities or effects the card has. (Include just the type, not the actual ability or effect.) | Once per Turn Action, Instant |
| Ability and Effect Keywords | string[] | A list of any keywords the card's abilities or effects have. (Do not include keywords the card grants or removes from other cards.) | Attack, Go again |
| Granted Keywords | string[] | A list of keywords that the card grants (conditionally or unconditionally) to **other** cards. | Dominate |
| Functional Text | string | The functional text that effects gameplay. Use the text from the latest printing or errata. Use [Markdown](https://www.markdownguide.org/basic-syntax/) for bold, italic, etc., and use the list of game icon representations below for representing attack icons, defense icons, etc. | **Combo** - If Surging Strike was the last attack this combat chain, Whelming Gustwave gains +1{p}, **go again**, and "If this hits, draw a card." |
| Flavor Text | string | Any flavor text that appears on the latest printing of the card with flavor text. Do not use italics on this, text is assumed to be in italics. (Example pulled from Talisman of Warfare.) | It's said that wherever the Dracai of War planted this talisman, the lava was soon to flow. |
| Type Text | string | The type text as printed on the latest edition of the card. | Ninja Action - Attack |
| Artists | string[] | The artists of the card. If there is only one artist for all versions of the cards, just one artist should be listed. If there are multiple artists, the artists are each listed per cardId (repeated as necessary), correlated to the Identifiers field. If an artist was changed mid printing, instead use the format ``{Arist Name} - {Card Identifier} - {Set Edition Shorthand}` for all artists. | Agri Karuniawan, Arif Wijaya, Arif Wijaya, Arif Wijaya, Arif Wijaya |
| Card Played Horizontally | bool | Is the card played horizontally (Ex: Landmarks)? No value is considered No. | Yes |
| Blitz Legal | bool | Is the card initially legal in the Blitz format? No given value is considered Yes. | Yes |
| CC Legal | bool | Is the card initially legal in the Classic Constructed format? No given value is considered Yes. | Yes |
| Commoner Legal | bool | Is the card initially legal in the Commoner format? No given value is considered Yes. | Yes |
| Blitz Living Legend | datetime | The date the card was or will be a Living Legend in the Blitz format. No given value means the card is not a Living Legend. | 2021-12-01T00:00:00.000Z |
| CC Living Legend | datetime | The date the card was or will be a Living Legend in the Classic Constructed format. No given value means the card is not a Living Legend. | 2021-12-01T00:00:00.000Z |
| Blitz Banned | datetime | The date the card was or will be banned in the Blitz format. No given value means the card is not banned. | 2021-12-01T00:00:00.000Z |
| CC Banned | datetime | The date the card was or will be banned in the Classic Constructed format. No given value means the card is not banned. | 2021-12-01T00:00:00.000Z |
| Commoner Banned | datetime | The date the card was or will be banned in the Commoner format. No given value means the card is not banned. | 2021-12-01T00:00:00.000Z |
| Blitz Suspended Start | datetime | The date the card was or will be suspended in the Blitz format. No given value means the card is not suspended. | 2021-12-01T00:00:00.000Z |
| Blitz Suspended End | string | Info on when the card is planned to be unsuspended in the Blitz format. No given value means the card is not suspended. | Until Chane hits Living Legend |
| CC Suspended Start | datetime | The date the card was or will be suspended in the Classic Constructed format. No given value means the card is not suspended. | 2021-12-01T00:00:00.000Z |
| CC Suspended End | string | Info on when the card is planned to be unsuspended in the Classic Constructed format. No given value means the card is not suspended. | Until Chane, Bound by Shadow hits Living Legend |
| Commoner Suspended Start | datetime | The date the card was or will be suspended in the Commoner format. No given value means the card is not suspended. | 2021-12-01T00:00:00.000Z |
| Commoner Suspended End | string | Info on when the card is planned to be unsuspended in the Commoner format. No given value means the card is not suspended. | Until April 29, 2022 |
| Variations | string[] | The list of foilings the card is available in within a set/edition combination, as well as any alternate arts for the card. The [Collector's Center](https://fabtcg.com/collectors-centre/) has good resources for finding details on this. If there is an alternate art, make a separate entry in this array and tack on the shorthand for the alternate art type. Format: `{Foiling Shorthands separated by spaces} - {Card Identifier} - {Set Edition Shorthand} (- {Alternate Art Shorthand})` (Using Channel Lake Frigid in this example.) | S R - ELE146 - F, R - ELE146 - F - AA, S R - ELE146 - U |
| Image URLs | string[] | Links to images from fabtcg.com's [image galleries](https://fabtcg.com/resources/card-galleries/) for a set/edition combination. If there is an alternate art, make a separate entry in this array and tack on the shorthand for the alternate art type. Format: `{Image URL} - {Card Identifier} - {Set Edition Shorthand} (- {Alternate Art Shorthand})` (Using Channel Lake Frigid in this example.) | https://storage.googleapis.com/fabmaster/media/images/ELE146.width-450.png - ELE146 - F, https://product-images.tcgplayer.com/fit-in/400x558/248564.jpg - ELE146 - F - AA, https://storage.googleapis.com/fabmaster/media/images/U-ELE146.width-450.png - ELE146 - U |

Note: Cards are organized by what main set they were initially released in, in order of release. If they were never released in a main set, they are organized by non-set/promo in order of release.


### Rarity
| Field Name | Intended Data Type | Explanation | Example |
| --- | --- | --- | --- |
| Shorthand | string | Shorthand representation of the rarity, intended for quick typing and correlating between other CSVs. | M |
| Text | string | Full name of the rarity. | Majestic |


### Icon
| Field Name | Intended Data Type | Explanation | Example |
| --- | --- | --- | --- |
| Shorthand | string | Shorthand representation of the icon, intended for representing the icon in effect text and correlating between other CSVs. When displaying text in an app, search for this to replace with the actual icon. | {p} |
| Name | string | Name of the icon. | Attack |
| Image URL | string | Url to the icon. | TODO |


### Keyword
| Field Name | Intended Data Type | Explanation | Example |
| --- | --- | --- | --- |
| Name | string | Name of the keyword. | Battleworn |
| Description | string | Description of the keyword's meaning. | TODO |


### Type
| Field Name | Intended Data Type | Explanation | Example |
| --- | --- | --- | --- |
| Name | string | Name of the type. | Attack |


### Foiling
| Field Name | Intended Data Type | Explanation | Example |
| --- | --- | --- | --- |
| Shorthand | string | Shorthand representation of the foiling. | R |
| Name | string | Name of the foiling. | Rainbow Foil |


### Edition
| Field Name | Intended Data Type | Explanation | Example |
| --- | --- | --- | --- |
| Shorthand | string | Shorthand representation of the edition. | U |
| Name | string | Name of the edition. | Unlimited Edition |

### Artist
| Field Name | Intended Data Type | Explanation | Example |
| --- | --- | --- | --- |
| Name | string | Name of the artist. | Saad Irfan  |


## Abbreviations

### Rarity (Shorthand - Text)
* C - Common
* R - Rare
* S - Super Rare
* M - Majestic
* L - Legendary
* F - Fabled
* T - Token
* V - Marvel
* P - Promo


### Icons (Shorthand - Name)
* {r}  - Resource Point
* {p} - Power
* {d} - Defense Value
* {h} - Life (of a hero card)
* {i} - Intellect (of a hero card)


### Foiling (Shorthand - Name)
* S - Standard
* R - Rainbow Foil
* C - Cold Foil
* G - Gold Cold Foil


### Edition (Shorthand - Name)
* A - Alpha
* F - First
* U - Unlimited
* N - No specified edition (used for promos, non-set releases, etc.)


### Alternate Art Variations (Shorthand - Name)
* AA - Alternate Art
* AT - Alternate Text
* EA - Extended Art
* FA - Full Art
