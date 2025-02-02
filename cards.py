from lib import log



class Tracker_Card:
    def __init__(self, card: str):
        self.card: str = card
        self.player: str = ''
        self.antiPlayers: list[str] = []

    def trackPlayer(self, playername: str) -> None:
        self.player = playername

    def trackAntiPlayer(self, playername: str) -> None:
        if playername not in self.antiPlayers: self.antiPlayers.append(playername)

    def getAntiPlayers(self) -> list[str]:
        return self.antiPlayers
    
class Tracker:
    def __init__(self):
        self.cards: dict[str, Tracker_Card] = {card:Tracker_Card(card) for card in RAWCARDS}

    # initialises the tracker to include a players hand
    def loadHand(self, playername: str, hand: list[Tracker_Card]) -> None:
        for card in hand: self.cards[card].player = playername

    # when a player passes, track that they do not have a card
    def trackAntiCard(self, playername: str, card: str) -> None:
        self.cards[card].trackAntiPlayer(playername)

    def trackAntiCards(self, playername: str, cards: list[str]) -> None:
        for card in cards: self.trackAntiCard(playername, card)

    # when a card has been seen, track the player that showed it
    def trackCard(self, playername: str, card: str) -> None:
        self.cards[card].trackPlayer(playername)

    def trackCards(self, playername: str, cards: list[str]) -> None:
        for card in cards: self.trackCard(playername, card)

    # reutrns a specific tracker card which has additional information
    def getCard(self, card: str) -> Tracker_Card:
        return self.cards[card]

    def getAllCards(self) -> list[Tracker_Card]:
        return list(self.cards.values())

    def getUnknowns(self) -> dict[str, list]:
        unknowns: list[str] = []

        for tracker_card in self.cards.values():
            if tracker_card.player == '':
                unknowns.append(tracker_card.card)

        return categorise(unknowns)



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

def categorise(cards: list[str]) -> dict[str, list]:
    categorised = {key:[] for key in cardDict}

    for card in cards:
        for category in cardDict:
            if card in cardDict[category]:
                categorised[category].append(card)

    return categorised



cardDict = {'people':  ['mustard','scarlet','green','white','plum','peacock'],
            'rooms':   ['study','observatory','kitchen','living room','dining room','library','patio','pool'],
            'weapons': ['knife','wrench','poison','axe','bat', 'pistol','candlestick']}

RAWCARDS = [card for cards in cardDict.values() for card in cards]
numCards = len(RAWCARDS)


if __name__ == "__main__":
    print(RAWCARDS)