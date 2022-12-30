# CSV Schemas

The CSVs are tab delimited and use " as string indicators.

## Set
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



## Card
| Field Name | Intended Data Type | Explanation | Example |
| --- | --- | --- | --- |
| Unique ID | string | The unique identifier for this card within the data set. This is generated by a script, do not manually fill this out. | nM8BHGHd9qLGTPgwtWzkJ |
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
| Variation Unique IDs | string[] | The unique identifiers for this card's variations within the data set. This is generated by a script, do not manually fill this out. | d87QcRDq6rLqD86pG6H8C – 1HP397 – N, LHFWfJHzHMJkLnMBmbJQp – WTR192 – A, HbtNt6M8NkMWLTLfJFWRW – WTR192 – U, RLM9MbnpqjJCwQtLBnKRg – UPR210 – N |
| Image URLs | string[] | Links to images from fabtcg.com's [image galleries](https://fabtcg.com/resources/card-galleries/) for a set/edition combination. If there is an alternate art, make a separate entry in this array and tack on the shorthand for the alternate art type. Format: `{Image URL} - {Card Identifier} - {Set Edition Shorthand} (- {Alternate Art Shorthand})` (Using Channel Lake Frigid in this example.) | https://storage.googleapis.com/fabmaster/media/images/ELE146.width-450.png - ELE146 - F, https://product-images.tcgplayer.com/fit-in/400x558/248564.jpg - ELE146 - F - AA, https://storage.googleapis.com/fabmaster/media/images/U-ELE146.width-450.png - ELE146 - U |

Note: Cards are organized by what main set they were initially released in, in order of release. If they were never released in a main set, they are organized by non-set/promo in order of release.


## Rarity
| Field Name | Intended Data Type | Explanation | Example |
| --- | --- | --- | --- |
| Shorthand | string | Shorthand representation of the rarity, intended for quick typing and correlating between other CSVs. | M |
| Text | string | Full name of the rarity. | Majestic |


## Icon
| Field Name | Intended Data Type | Explanation | Example |
| --- | --- | --- | --- |
| Shorthand | string | Shorthand representation of the icon, intended for representing the icon in effect text and correlating between other CSVs. When displaying text in an app, search for this to replace with the actual icon. | {p} |
| Name | string | Name of the icon. | Attack |
| Image URL | string | Url to the icon. | TODO |


## Keyword
| Field Name | Intended Data Type | Explanation | Example |
| --- | --- | --- | --- |
| Name | string | Name of the keyword. | Battleworn |
| Description | string | Description of the keyword's meaning. | TODO |


## Type
| Field Name | Intended Data Type | Explanation | Example |
| --- | --- | --- | --- |
| Name | string | Name of the type. | Attack |


## Foiling
| Field Name | Intended Data Type | Explanation | Example |
| --- | --- | --- | --- |
| Shorthand | string | Shorthand representation of the foiling. | R |
| Name | string | Name of the foiling. | Rainbow Foil |


## Edition
| Field Name | Intended Data Type | Explanation | Example |
| --- | --- | --- | --- |
| Shorthand | string | Shorthand representation of the edition. | U |
| Name | string | Name of the edition. | Unlimited Edition |

## Artist
| Field Name | Intended Data Type | Explanation | Example |
| --- | --- | --- | --- |
| Name | string | Name of the artist. | Saad Irfan  |

