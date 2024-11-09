
from typing import List, Dict



class Tracker_Card:
    def __init__(self, card: str):
        self.card: str = card
        self.player: str = ''
        self.antiPlayers: List[str] = []

    def setPlayer(self, playername: str):
        if playername != self.player: self.player = playername

    def addAntiPlayer(self, playername: str):
        if playername not in self.antiPlayers: self.antiPlayers.append(playername)

    def getAntiCards(self):
        return self.antiPlayers
    
class Tracker:
    def __init__(self):
        self.cards: Dict[str, Tracker_Card] = {card:Tracker_Card(card) for card in RAWCARDS}

    # initialises the tracker to include a players hand
    def loadHand(self, hand: List[Tracker_Card], playername):
        for card in hand:
            self.cards[card].player = playername

    def addAntiCard(self, card: str, playername: str):
        self.cards[card].addAntiPlayer(playername)

    def addAntiCards(self, cards: List[str], playername: str):
        for card in cards:
            self.addAntiCard(card, playername)

    def addCard(self, card: str, playername: str):
        self.cards[card].setPlayer(playername)

    def getCard(self, card: str) -> Tracker_Card:
        return self.cards[card]

    def getCards(self) -> List[Tracker_Card]:
        return list(self.cards.values())



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



cardDict = {'people':  ['mustard','scarlet','green','white','plum','peacock'],
            'rooms':   ['study','observatory','kitchen','living room','dining room','library','patio','pool'],
            'weapons': ['knife','wrench','poison','axe','bat','candlestick']}

RAWCARDS = []
for key in cardDict: RAWCARDS += cardDict[key]

numCards = len(RAWCARDS)
