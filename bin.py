
class Profile:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.antiCards = []

    def addCard(self, card):
        if card not in self.hand:
            self.hand.append(card)

    def addAntiCard(self, card):
        if card not in self.antiCards:
            self.antiCards.append(card)

    def addAntiCards(self, cards: list):
        for card in cards:
            self.addAntiCard(card)

    def print(self, playerName: str):
        print(f" - {playerName}'s profile of {self.name}")
        print(f"Hand: {self.hand}")
        print(f"Anti cards: {self.antiCards}")

