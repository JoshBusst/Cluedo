from cards import *
from players import *
from typing import List, Dict


DONTPRINT: bool = 0



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
        
        self.playernames: List[str] = names
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

    def getKnownCards(self) -> List[str]:
        items = self.tracker.getCards()
        cards = [card.card for card in items if card.player != '']

        return cards 
    
    def getUnknownCards(self) -> List[str]:
        knowns = self.getKnownCards()
        unknowns = [card for card in RAWCARDS if card not in knowns]

        return unknowns

    def startRumour(self):
        unknowns: dict = categorise(self.getUnknownCards())
        rumour = edict()

        for key in unknowns:
            if len(unknowns[key]) == 0: rumour[key] = pickrandom(cardDict[key])
            else:                       rumour[key] = pickrandom(unknowns[key])

        return rumour

    def seeCard(self, card, playername: str):
        self.tracker.addCard(card, playername)

    def seeAntiCards(self, rumour: dict, playername: str):
        self.tracker.addAntiCards(rumour.values(), playername)

    def printProfile(self, playername: str):
        hand = [card.card for card in self.tracker.cards.values() if card.player == playername]
        antiCards = [card.card for card in self.tracker.cards.values() if playername in card.antiPlayers]
        
        print(playername)
        print(f"Hand: {hand}\nAntiCards: {antiCards}\n")
    
    def setHand(self, hand: List[str]):
        self.hand = hand
        self.tracker.loadHand(hand, self.name)

    def printAllProfiles(self):
        print(f"\n{self.name}'s profiles")

        for playername in self.playernames:
            self.printProfile(playername)


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
                               f"*Please select a valid room from: {cardDict['rooms']}")

        weapon = self.getInput(cardDict['weapons'],
                               "Please input a murder weapon.",
                               f"*Please select a valid weapon from: {cardDict['weapons']}")
        
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

    def addAccusation(self, playername: str, accusation: Dict[str, str]):
        pass

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
        players[i].setHand(hand)

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

def nextPlayers(index: int):
    return [players[(i + index + 1) % numPlayers] for i in range(numPlayers - 1)]
            
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
        global players, numPlayers, turn
        players = [player for player in players if player.name != name]
        numPlayers -= 1
        turn -= 1

def formatRumour(playername: str, rumour: Dict[str,str]):
    return "%s thinks it was %s in the %s with the %s." %(playername, *rumour.values())

def startRumour(player):
    if player.ishuman:
        raise ValueError
    else:
        rumour = player.startRumour()
        player.printRumour(rumour)
        events.addRumour(player.name, rumour)

    for playerAsked in nextPlayers(turn):
        if playerAsked.hasCards(rumour):
            showCard(playerAsked, player, rumour)
            events.addShow(playerAsked.name)
            break
        else:
            showAntiCards(playerAsked, player, rumour)
            events.addPass(playerAsked.name)




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
    for i in range(100):
        if gameover:
            break

        currentPlayer = players[turn]
        consoleOut(f"{currentPlayer.name}'s turn!", "It's")

        action = currentPlayer.turn()

        if action == 1: # start rumour
            startRumour(currentPlayer)
        elif action == 2: # accuse
            pass
        else:
            print(action)
            raise ValueError

        turn = (turn + 1) % numPlayers

        if numPlayers == 1:
            consoleOut(f"{players[0].name} wins the game! By default :/", ">#")
            exit()
        elif numPlayers <= 0:
            raise ValueError

    consoleOut(f"Turns taken: {i}", ">>:")