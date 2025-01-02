
class Tracker_Card:
    def __init__(self, card: str):
        self.card: str = card
        self.player: str = ''
        self.antiPlayers: list[str] = []

    def setPlayer(self, playername: str) -> None:
        if playername != self.player: self.player = playername

    def addAntiPlayer(self, playername: str) -> None:
        if playername not in self.antiPlayers: self.antiPlayers.append(playername)

    def getAntiPlayers(self) -> list[str]:
        return self.antiPlayers
    
class Tracker:
    def __init__(self):
        self.cards: dict[str, Tracker_Card] = {card:Tracker_Card(card) for card in RAWCARDS}

    # initialises the tracker to include a players hand
    def loadHand(self, playername: str, hand: list[Tracker_Card]) -> None:
        for card in hand: self.cards[card].player = playername

    def addAntiCard(self, playername: str, card: str) -> None:
        self.cards[card].addAntiPlayer(playername)

    def addAntiCards(self, playername: str, cards: list[str]) -> None:
        for card in cards: self.addAntiCard(playername, card)

    def addCard(self, playername: str, card: str) -> None:
        self.cards[card].setPlayer(playername)

    # reutrns a specific tracker card which has additional information
    def getCard(self, card: str) -> Tracker_Card:
        return self.cards[card]

    def getAllCards(self) -> list[Tracker_Card]:
        return list(self.cards.values())



def isperson(card) -> bool:
    return card in cardDict['people']

def isroom(card) -> bool:
    return card in cardDict['room']

def isweapon(card) -> bool:
    return card in cardDict['weapons']

def cardtype(card) -> str:
    for key in cardDict:
        if card in cardDict[key]:
            return key

def edict() -> dict[str, str]:
    return {key:'' for key in cardDict}

def iscard(card: str) -> bool:
    return card in RAWCARDS

def categorise(cards: list) -> dict[str, list]:
    categorised = {key:[] for key in cardDict}

    for card in cards:
        for category in cardDict:
            if card in cardDict[category]:
                categorised[category].append(card)

    return categorised



cardDict = {'people':  ['mustard','scarlet','green','white','plum','peacock'],
            'rooms':   ['study','observatory','kitchen','living room','dining room','library','patio','pool'],
            'weapons': ['knife','wrench','poison','axe','bat','candlestick']}

RAWCARDS = [card for cards in cardDict.values() for card in cards]
numCards = len(RAWCARDS)


if __name__ == "__main__":
    print(RAWCARDS)