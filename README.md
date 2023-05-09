# Notes
## Source for combos, re-fetch every so often
https://edhrec.com/data/spellbook_counts.json

## Source for full DB of Magic cards
https://mtgjson.com/downloads/all-files/

## Structure of collections files
"<count> <card name>"
regexp: `^(\d+)\s([^(]+)\s.+`

## Structure of combos.json
```python
x = \
{
    "combos": {
        "int": {
            "cardnames": ["a", "b", "c"]
        }       
    }
}
```

## Structure of each card in AtomicCards.json (from mtgjson)
* Fields we care about
    * colorIdentity
    * colors
    * convertedManaCost
    * keywords
    * manaCost
    * manaValue
    * power
    * subtypes
    * supertypes
    * text
    * toughness
    * type
    * types
    
    
```python
x = \
{'colorIdentity': ['B', 'R', 'W'],
 'colors': ['B', 'R', 'W'],
 'convertedManaCost': 5.0,
 'edhrecRank': 6582,
 'edhrecSaltiness': 0.23,
 'firstPrinting': 'KTK',
 'foreignData': [{'language': 'Japanese',
                  'name': '兜砕きのズルゴ',
                  'text': '速攻\n'
                          '兜砕きのズルゴは可能なら各戦闘で攻撃する。\n'
                          'あなたのターンであるかぎり、兜砕きのズルゴは破壊不能を持つ。\n'
                          'このターンに兜砕きのズルゴによってダメージを与えられたクリーチャーが１体死亡するたび、兜砕きのズルゴの上に＋１/＋１カウンターを１個置く。',
                  'type': '伝説のクリーチャー — オーク・戦士'}],
 'identifiers': {'scryfallOracleId': '6c48d888-9f5d-43f4-adbd-61dbdba09260'},
 'keywords': ['Haste'],
 'layout': 'normal',
 'leadershipSkills': {'brawl': False, 'commander': True, 'oathbreaker': False},
 'legalities': {'commander': 'Legal',
                'duel': 'Legal',
                'legacy': 'Legal',
                'modern': 'Legal',
                'oathbreaker': 'Legal',
                'penny': 'Legal',
                'pioneer': 'Legal',
                'vintage': 'Legal'},
 'manaCost': '{2}{R}{W}{B}',
 'manaValue': 5.0,
 'name': 'Zurgo Helmsmasher',
 'power': '7',
 'printings': ['DDN', 'KTK', 'PKTK', 'PRM', 'SLD'],
 'purchaseUrls': {'cardKingdom': 'https://mtgjson.com/links/01738265abb38587',
                  'cardKingdomFoil': 'https://mtgjson.com/links/4ee0162139c3b93f',
                  'cardmarket': 'https://mtgjson.com/links/1b4a5e9a427dc06e',
                  'tcgplayer': 'https://mtgjson.com/links/87d50fd03b1581fa'},
 'rulings': [{'date': '2014-09-20',
              'text': 'You still choose which player or planeswalker Zurgo '
                      'Helmsmasher attacks.'},
             {'date': '2014-09-20',
              'text': 'If, during your declare attackers step, Zurgo is tapped '
                      'or is affected by a spell or ability that says it can’t '
                      'attack, then it doesn’t attack. If there’s a cost '
                      'associated with having Zurgo attack, you aren’t forced '
                      'to pay that cost, so it doesn’t have to attack in that '
                      'case either.'},
             {'date': '2014-09-20',
              'text': 'If Zurgo enters the battlefield before the combat '
                      'phase, it will attack that turn if able. If it enters '
                      'the battlefield after combat, it won’t attack that turn '
                      'and will usually be available to block on the following '
                      'turn.'},
             {'date': '2014-09-20',
              'text': 'Each time a creature dies, check whether Zurgo had '
                      'dealt any damage to it at any time during that turn. If '
                      'so, Zurgo’s ability will trigger. It doesn’t matter who '
                      'controlled the creature or whose graveyard it went '
                      'to.'}],
 'subtypes': ['Orc', 'Warrior'],
 'supertypes': ['Legendary'],
 'text': 'Haste\n'
         'Zurgo Helmsmasher attacks each combat if able.\n'
         "Zurgo Helmsmasher has indestructible as long as it's your turn.\n"
         'Whenever a creature dealt damage by Zurgo Helmsmasher this turn '
         'dies, put a +1/+1 counter on Zurgo Helmsmasher.',
 'toughness': '2',
 'type': 'Legendary Creature — Orc Warrior',
 'types': ['Creature']}
```
