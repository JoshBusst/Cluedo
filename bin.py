
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





class Agent(Player):
    def __init__(self, name: str, names: list, ishuman: bool):
        Player.__init__(self, name, names, ishuman)
        
        self.playernames: list[str] = names
        self.tracker: Tracker = Tracker()

    def turn(self):
        # return 1 for rumour and 2 for accusation

        # collate list of all cards that are known to be held by no one
        cards = self.tracker.getCards()
        antiCards = [card.card for card in cards if len(card.antiPlayers) == numPlayers - 1]

        # if some cards arent held by anyone, these are the centre cards
        if len(antiCards) >= 3:
            answer = categorise(antiCards)

            # if all answers are found, accuse
            if all([val != [] for val in answer.values()]):
                answer = {key:answer[key][0] for key in answer}
                # accuse(self.name, answer)

                return 2, answer
        else:
            # no accusation. deduce from previous rumours
            tracker = self.tracker.cards
            updated = True

            while updated:
                updated = False

                for event in events.getall():
                    playerAnswered = event.playername
                    rumour = event.rumourCards()
                    
                    # skip if player who answered is known to hold any of the rumour cards
                    if any([playerAnswered == tracker[card].player for card in rumour]): continue

                    # skip if player deducing holds any of the rumour cards
                    if any([self.name == tracker[card].player for card in rumour]): continue

                    rumour = [card for card in rumour if tracker[card].player == '']
                    rumour = [card for card in rumour if playerAnswered not in tracker[card].getAntiCards()]

                    if len(rumour) == 1:
                        card = rumour[0]
                        tracker[card].player = playerAnswered
                        updated = True

        return 1, self.startRumour()

    def getKnownCards(self) -> list[str]:
        items = self.tracker.getCards()
        cards = [card.card for card in items if card.player != '']

        return cards 
    
    def getUnknownCards(self) -> list[str]:
        knowns = self.getKnownCards()
        unknowns = [card for card in RAWCARDS if card not in knowns]

        return unknowns

    def startRumour(self):
        unknowns: dict = categorise(self.getUnknownCards())
        rumour = edict()

        for key in unknowns:
            if len(unknowns[key]) == 0: rumour[key] = pickrandom(carddict[key])
            else:                       rumour[key] = pickrandom(unknowns[key])

        return rumour

    def recordCard(self, playername: str, card: str) -> None:
        self.tracker.addCard(playername, card)

    def recordPass(self, playername: str, rumour: dict) -> None:
        self.tracker.addAntiCards(rumour.values(), playername)

    def printProfile(self, playername: str):
        hand = [card.card for card in self.tracker.cards.values() if card.player == playername]
        antiCards = [card.card for card in self.tracker.cards.values() if playername in card.antiPlayers]
        
        print(playername)
        print(f"Hand: {hand}\nAntiCards: {antiCards}\n")
    
    def setHand(self, hand: list[str]):
        self.hand = hand
        self.tracker.loadHand(hand, self.name)

    def printAllProfiles(self):
        print(f"\n{self.name}'s profiles")

        for playername in self.playernames:
            self.printProfile(playername)
