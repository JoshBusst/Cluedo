from cards import *
from typing import List, Dict
from abc import abstractmethod


DONTPRINT: bool = 0



class Event:
    def __init__(self, playername: str='', rumour: Dict[str,str]={}):
        self.playername = playername
        self.rumour: Dict[str,str] = rumour
        self.passes: List[str] = []
        self.whoShowed: str = None

    def formatRumour(self):
        return formatRumour(self.playername, self.rumour)

    def print(self):
        print(f" >>: {self.formatRumour()}")
        print(f" > Passes: {self.passes}")
        print(f" > Who showed: {self.whoShowed}")

    def rumourCards(self):
        return list(self.rumour.values())
    
class Events:
    def __init__(self):
        self.history: List[Event] = []
        self.len: int = 0

    def addRumour(self, playername, rumour):
        event = Event(playername, rumour)

        self.history.append(event)
        self.len += 1

    def addPass(self, playername):
        self.history[-1].passes.append(playername)

    def addShow(self, playername):
        self.history[-1].whoShowed = playername

    def delete(self):
        pass

    def get(self, i):
        assert(i >= 0 and i < self.len)
        return self.history[i]
    
    def getlast(self):
        return self.history[-1]
    
    def getfrom(self, i):
        assert(i >= 0 and i < self.len)
        return self.history[i:]
    
    def getto(self, i):
        assert(i >= 0 and i < self.len)
        return self.history[:i]
    
    def getall(self):
        return self.history

    def print(self, i: int):
        self.get(i).print()



class Tracker_Card:
    def __init__(self, card: str):
        self.card: str = card
        self.player: str = ''
        self.antiPlayers: List[str] = []

    def setPlayer(self, playername: str):
        if playername != self.player: self.player = playername

    def addAntiPlayer(self, playername: str):
        if playername not in self.antiPlayers: self.antiPlayers.append(playername)

class Tracker:
    def __init__(self):
        self.cards: Dict[str, Tracker_Card] = {card:Tracker_Card(card) for card in RAWCARDS}

    def addAntiCard(self, card: str, playername: str):
        self.cards[card].addAntiPlayer(playername)

    def cardHeldBy(self, card: str, playername: str):
        self.cards[card].setPlayer(playername)

    def getCard(self, card: str) -> Tracker_Card:
        return self.cards[card]

    def getCards(self) -> List[Tracker_Card]:
        return list(self.cards.values())



class Player:
    def __init__(self, name: str, names: list, ishuman: bool):
        self.name: str = name
        self.hand: list = []
        self.ishuman: bool = ishuman

    @abstractmethod
    def seeCard(self, card, playerName: str):
        pass

    @abstractmethod
    def startRumour(self):
        pass

    @abstractmethod
    def turn(self) -> bool:
        pass

    def hasCards(self, rumour: Dict[str,str]):
        return any([card in self.hand for card in rumour.values()])
        
    def hasCard(self, card: str):
        return card in self.hand


    def printRumour(self, rumour: dict):
        consoleOut(formatRumour(self.name, rumour), '>>:')
        
    def printHand(self):
        consoleOut(f"{self.name}'s hand: {self.hand}")

        

class Agent(Player):
    def __init__(self, name: str, names: list, ishuman: bool):
        Player.__init__(self, name, names, ishuman)
        
        self.profileNames: List[str] = names
        self.tracker: Tracker = Tracker()

    def turn(self):
        # deduce if any cards are held by no one
        # antiCards = [card for card in RAWCARDS if card not in self.hand]
        # for profile in self.profiles.values():
        #     antiCards = [card for card in profile.antiCards if card in antiCards]

        #     if len(antiCards) == 0:
        #         break

        for card in self.tracker.getCards():
            if len(card.antiPlayers) == numCards - 1:
                pass

        # if some cards arent held by anyone, these are the centre cards
        if len(antiCards) > 0:
            answer = categorise(antiCards)

            # if all answers are found, accuse
            if all([val != [] for val in answer.values()]):
                answer = {key:answer[key][0] for key in answer}
                accuse(self.name, answer)

                return True
        else:
            # no accusation. deduce from previous rumours
            self.deduction()

    def deduction(self):
        # consoleOut(f"{self.name} is making a deduction", "[.]>")
        cardTracker = self.getCardTracker()

        updated = True

        while updated:
            updated = False

            for event in events.getall():
                playerAnswered = event.playername
                rumour = event.rumourCards()
                
                # skip if player answering is known to hold any of the rumour cards
                if any([playerAnswered == cardTracker[card][0] for card in rumour]): continue

                # skip if player deducing holds any of the rumour cards
                if any([self.name == cardTracker[card][0] for card in rumour]): continue

                rumour = [card for card in rumour if cardTracker[card][0] == '']
                rumour = [card for card in rumour if playerAnswered not in cardTracker[card][1]]

                if len(rumour) == 1:
                    card = rumour[0]
                    cardTracker[card][0] = playerAnswered
                    updated = True

    def getCardTracker(self):
        tracker: Dict[str,str] = {key:['',[]] for key in RAWCARDS} # key:[cardHolder, [antiCardHolders]]
        
        # knowns = [[profile.name, profile.hand] for profile in self.profiles.values()]
        # antiCards = [[profile.name, profile.antiCards] for profile in self.profiles.values()]

        # for playername, cards in knowns:
        #     for card in cards:
        #         tracker[card] = playername

        for profile in self.profiles.values():
            for card in profile.hand:
                tracker[card][0] = profile.name

            for card in profile.antiCards:
                tracker[card][1].append(profile.name)

        return tracker

    def getKnownCards(self):
        # cards = []

        # for name in self.profiles:
        #     cards += self.profiles[name].hand

        # cards += self.hand

        knownCards: Dict[str,str] = {}
        cardPairs = [[profile.name, profile.hand] for profile in self.profiles.values()]

        for playername, cards in cardPairs:
            for card in cards:
                knownCards[card] = playername

        return knownCards
    
    def getUnknownCards(self):
        knowns = list(self.getKnownCards().keys())
        unknowns = [card for card in RAWCARDS if card not in knowns]

        return unknowns

    def startRumour(self):
        unknowns: dict = categorise(self.getUnknownCards())
        rumour = edict()

        for key in unknowns:
            if len(unknowns[key]) == 0:
                # rand = randint(0, len(cardDict[key]) - 1)
                rumour[key] = pickrandom(cardDict[key])
            else:
                # rand = randint(0, len(unknowns[key]) - 1)
                rumour[key] = pickrandom(unknowns[key])

        return rumour

    def seeCard(self, card, playerName: str):
        self.profiles[playerName].addCard(card)

    def seeAntiCards(self, rumour: dict, playerName: str):
        self.profiles[playerName].addAntiCards(rumour.values())

    def printProfile(self, playerName: str):
        self.profiles[playerName].print(self.name)

    def printAllProfiles(self):
        for profile in self.profiles.values():
            profile.print(self.name)



class Human(Player):
    def __init__(self, name, names, ishuman):
        Player.__init__(self, name, names, ishuman)

    def seeCard(self, card, playerName: str):
        consoleOut(f"{playerName} shows you the card {card}")

    def startRumour(self):
        person = self.getInput(cardDict['people'],
                               "Please accuse a person.",
                               f"*Please select a valid player name from: {cardDict['people']}.")
        
        room = self.getInput(cardDict['rooms'],
                               "Please input a room.",
                               f"Please select a valid room from: {cardDict['rooms']}")

        weapon = self.getInput(cardDict['weapons'],
                               "Please input a murder weapon.",
                               f"Please select a valid weapon from: {cardDict['weapons']}")
        
        return {'people': person, 'rooms': room, 'weapons': weapon}

    def turn(self):
        pass
    
    def getInput(self, list, startMsg, errorMsg):
        consoleOut(startMsg)
        info = input(">_ ").lower()

        while info not in list:
            consoleOut(errorMsg)
            info = input(">_ ").lower()

        return info



def loadPlayers(names) -> List[Player]:
    return [Agent(name, names, False) for name in names]

def dealcards(players) -> List[str]:
    from random import shuffle
    from copy import copy

    cards = copy(RAWCARDS)
    shuffle(cards)

    # categorise shuffled list and take first entry of each category
    centreCardsDict = categorise(cards)
    centreCards = [lst[0] for lst in centreCardsDict.values()]

    # remove three centre cards from dealable cards
    cards = [card for card in cards if card not in centreCards]


    numPlayers = len(players)
    deal = [[] for _ in range(numPlayers)]

    for i, card in enumerate(cards):
        deal[i % numPlayers].append(card)

    for i, hand in enumerate(deal):
        players[i].hand = hand

    return centreCards

def showCard(p1: Player, p2: Player, rumour):
    from random import shuffle
    from copy import copy

    cards = copy(list(rumour.values()))
    shuffle(cards)

    card = None

    for card in cards:
        if card in p1.hand:
            break
        
    consoleOut(f"{p1.name} shows {p2.name} a card")
    p2.seeCard(card, p1.name)

def showAntiCards(p1: Player, p2: Player, rumour: Dict[str,str]):
        consoleOut(f"{p1.name} does not have a card.")
        p2.seeAntiCards(rumour, p1.name)

def nextPlayers(p1: Player):
    ind: int = players.index(p1) + 1
    return [players[(i + ind) % numPlayers] for i in range(numPlayers - 1)]
            
def consoleOut(msg: str, char: str=''):
    if DONTPRINT: return

    if char == '':
        print(f" - {msg}")
    else:
        print(f"\n {char} {msg}")

def accuse(name: str, accusation: Dict[str,str]):
    consoleOut("%s accuses %s in the %s with the %s!" %(name, *accusation.values()), '>!')

    if isequal(list(accusation.values()), centreCards):
        global gameover

        consoleOut(f"{name} wins the game!", '>#')
        gameover = True
    else:
        consoleOut(f"{name} has been murdered!", '>!')
        events.addAccusation(name, accusation)

        # player is removed from the game
        players = [player for player in players if player.name != name]
        numPlayers -= 1

def formatRumour(playername: str, rumour: Dict[str,str]):
    return "%s thinks it was %s in the %s with the %s." %(playername, *rumour.values())





from lib import *

events = Events()
playerNames = cardDict['people'][0:4]
players: List[Agent] = loadPlayers(playerNames)
numPlayers: int = len(playerNames)

gameover = False
turn = 0
currentPlayer = players[0]
centreCards = dealcards(players)



if __name__ == "__main__":
    for p in players:
        p.printHand()


    # while not gameover
    for i in range(100):
        if gameover:
            break

        currentPlayer = players[turn]
        consoleOut(f"{currentPlayer.name}'s turn!", "It's")

        playerAccused = currentPlayer.turn()

        # player accused and since the game is not over they must have failed
        if playerAccused:
            continue

        # start rumour
        if currentPlayer.ishuman:
            raise ValueError
        else:
            rumour = currentPlayer.startRumour()
            currentPlayer.printRumour(rumour)
            events.addRumour(currentPlayer.name, rumour)

        # ask players if they have cards
        for playerAsked in nextPlayers(currentPlayer):
            if playerAsked.hasCards(rumour):
                showCard(playerAsked, currentPlayer, rumour)
                events.addShow(playerAsked.name)
                break
            else:
                showAntiCards(playerAsked, currentPlayer, rumour)
                events.addPass(playerAsked.name)


        turn += 1
        if turn >= len(players): turn = 0


        # events.getlast().print()
        print()

    consoleOut(f"Turns taken: {i}", ">>:")