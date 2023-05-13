# Magic: The Gathering Deck Building Tool
The purpose of this project is to save time looking through your own collection for the cards you need to build a deck. Many of us diehard, long-time collectors have thousands of cards and it can be daunting to figure out what you can build from your own collection.

## How does it work?
### Data sources
This software takes 3 primary data sources and then provides you with simple commands to search for what you need.
* https://mtgjson.com - Provides a complete database of all MTG cards ever made and all of their details, structured as JSON
* https://edhrec.com - Provides structured list of combos that were submitted to the website
* Your collection in `<qty> <card name>` per line format. This can be in one or more files. Because of current limitations in MTG Arena, to export my own full collection, I had to save it in parts, one subset each in its own "deck" (e.g., Black commons, black rares, etc.) and then drop all those deck files into a single folder.

### Searches
#### Combo searches
Currently, we only store combos of 2, 3, or 4 cards. The data from EDHREC does have some larger combos, and we may add support for those later.
To search for combos, you need at least one card you want to find combos for, and then you can additionally add the following filters:
* `--include-colors "RGUBW"` - Specify to filter by cards that contain the specified colors
* `--exclude-colors "RGUBW"` - Specify to filter by cards that do not contain the specified colors. Passing all five colors to this argument will give you only combos with colorless cards.
* `--percent-in-collection` - Options are 25%, 50%, 75%, or 100%. 100% means only show combos that your collection has all cards for.

#### Common search types
All of the following search types can be filtered further by the filters noted above for combos.

##### Card draw
Search for spells that draw cards

##### Ramp
Search for spells that generate mana.
* `--gen-include-colors "RGUBW"` - Only return results that generate the specified colors of mana. Empty string would return only colorless mana generation.

##### Removal
Search for spells that remove opponents spells. By default
If none of the following are specified, all card types are included in results
* `--include-counter-spells`
* `--include-creature-removal`
* `--include-enchantment-removal`
* `--include-planeswalker-removal`
* `--include-artifact-removal`

If neither of the following is specified, both targeted and non-targeted will be included in results
* `--include-targeted` - "Destroy all non-land permanents"
* `--include-non-targeted` - "Destroy target creature"

If neither of the following is specified, both "destroy" and "exile" will be included in results
* `--include-exile`
* `--include-destroy`

#### Affinity types
At the top level you can break down types of play into format and metagame, but I wanted something a little bit more specific, so I'm calling it Affinity Type, here. So what is an Affinity Type? Here are some examples:
* Tribal
* Counters
* Creature tokens
* Sacrifice
* ETB (Enter the battlefield)
* Toxic (Poison)
* Defender
* Discard
* [Non-Creature Card type theme] Equipment, Aura, Enchantment, Artifact, Vehicle, Land
* [Keyword] (Goad, Lifelink, Mutate, Scry/Draw, X, Ninjutsu, Changeling, Mill, Boast, Foretell, Blitz)

Building a deck around one (or more) of the above mechanics is what I call an Affinity Type. This software will provide capability to search for cards that fit some subset of the above Affinity Types, eventually all of them and more.

So part of your deck-building strategy would work as follows:
1. Choose an Affinity Type
2. Choose your colors (some may work better than others for a given Affinity Type)
3. Search for cards in your collection for the specified Affinity Type
4. If it looks like there are enough, use that as your deck's starting point
5. Next, choose your meta, and MTGComboFinder

## Future improvements
* (high priority) Support registering cards from your physical collection. Currently only store for Arena.
* (high priority) Not all cards are in MTG Arena, and since that is the primary way in which I play, it would be helpful to be able to filter combos by those that only include Arena cards.
* (medium priority) Add support for > 4 card combos
* (low priority) Adding ID types from other databases (Scryfall, Card Kingdom, etc.)
* (low priority) Currently, I didn't want to deal with tracking which set each card is from, but since rarity varies based on set, it could be helpful to start including that.
