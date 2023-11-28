


cardDict = {'people':  ['mustard','scarlet','green','white','plum','peacock'],
            'rooms':   ['study','observatory','kitchen','living room','dining room','library','patio','pool'],
            'weapons': ['knife','wrench','poison','axe','bat','candlestick']}

RAWCARDS = []
for key in cardDict:
    RAWCARDS += cardDict[key]

numCards = len(RAWCARDS)


def isperson(card):
    return card in cardDict['people']

def isroom(card):
    return card in cardDict['room']

def isweapon(card):
    return card in cardDict['weapons']

def cardtype(card):
    for key in cardDict:
        if card in cardDict[key]:
            return key

def edict():
    return {key:None for key in cardDict}

def iscard(card: str):
    return card in rawCards

def categorise(cards: list):
    categorised = {key:[] for key in cardDict}

    for card in cards:
        for category in cardDict:
            if card in cardDict[category]:
                categorised[category].append(card)

    return categorised