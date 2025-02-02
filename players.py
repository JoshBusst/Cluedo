from abc import abstractmethod
from cards import *
from console import *
from lib import pickrandom, flatten

from random import shuffle



class Player:
    def __init__(self, name: str, ishuman: bool):
        self.name: str = name
        self.hand: list = []
        self.ishuman: bool = ishuman

    @abstractmethod
    def seeCard(self, playername: str, card: str) -> None:
        pass

    @abstractmethod
    def showCard(self, seerName: str, rumour: dict[str,str]) -> str:
        pass

    @abstractmethod
    def getRumour(self) -> dict[str,str]:
        pass

    @abstractmethod
    def getAccusation(self) -> dict[str,str]:
        pass

    @abstractmethod
    def setHand(self, hand: list[str]) -> None:
        pass

    def turn(self) -> int:
        pass

    def hasCards(self, rumour: dict[str,str]) -> bool:
        return any([card in self.hand for card in flatten(rumour.values())])
        
    def hasCard(self, card: str) -> bool:
        return card in self.hand
        
    def printHand(self) -> None:
        consoleOut(f"{self.name}'s hand: {self.hand}")



class Agent(Player):
    def __init__(self, name: str):
        Player.__init__(self, name, False)
        
        self.tracker: Tracker = Tracker()

    def seeCard(self, playername: str, card: str) -> None:
        self.tracker.trackCard(playername, card)

    def recordPass(self, playername: str, rumour: dict) -> None:
        self.tracker.trackAntiCards(playername, flatten(rumour.values()))
    
    # record when a player shows a card
    def recordShow(self, showername: str, seername: str, rumour: dict) -> None:
        pass #self.tracker.trackAntiCards(playername, rumour.values())

    def showCard(self, seerName: str, rumour: dict[str,str]) -> str:
        cardsHeld: list[str] = [card for card in flatten(rumour.values()) if card in self.hand]
        
        return pickrandom(cardsHeld)

    def setHand(self, hand: list[str]) -> None:
        self.hand = hand
        self.tracker.trackCards(self.name, hand)
        
    def getRumour(self) -> dict[str, str]:
        unknowns: dict[str, list] = self.tracker.getUnknowns()
        unknowns: list[list] = list(unknowns.values())

        rumour: dict[str, str] = categorise([pickrandom(unknowns[0]),
                                             pickrandom(unknowns[1]),
                                             pickrandom(unknowns[2])])
        
        return rumour

    def getAccusation(self) -> dict[str, str]:
        unknowns: dict[str, list] = self.tracker.getUnknowns()
        accusation: dict[str, str] = {'people':  unknowns['people'][0],
                                      'rooms':   unknowns['rooms'][0],
                                      'weapons': unknowns['weapons'][0]}
        return accusation

    def turn(self) -> int:
        unknowns: dict[str, list] = self.tracker.getUnknowns()
        log(unknowns)

        if all(len(seg) == 1 for seg in unknowns.values()):
            return 'a'
        else:
            return 'r'



class Human(Player):
    def __init__(self, name: str):
        Player.__init__(self, name, True)

    def setHand(self, hand: list[str]) -> None:
        self.hand = hand

    def seeCard(self, playername: str, card: str):
        consoleOut(f"{playername} shows you the card - {card}.")

    def showCard(self, seerName: str, rumour: dict[str,str]) -> str:
        cardsHeld: list[str] = [card for card in rumour.values() if card in self.hand]
        card: str = ''

        if len(cardsHeld) == 1:
            consoleOut(f"You showed {seerName} the card - {cardsHeld[0]}.")
            card = cardsHeld[0]
        else:
            card = getUserInput(cardsHeld, f"You're holding the cards {cardsHeld}. Which would you like to show to {seerName}?")
        
        return card

    def getRumour(self) -> dict[str, str]:
        person = getUserInput(cardDict['people'],  "Please input a persons name.")
        room   = getUserInput(cardDict['rooms'],   "Please input a room.")
        weapon = getUserInput(cardDict['weapons'], "Please input a murder weapon.")
        
        return {'people': person, 'rooms': room, 'weapons': weapon}

    def getAccusation(self) -> dict[str, str]:
        return self.getRumour()

    def turn(self) -> str:
        return getUserInput(['a','r'], "Would you like to accuse or start a rumour? a/r", "Please select a or r...")



# populates empty player spaces with agents and sets global variables. Returns a list of Player of size playerCount
# def loadPlayers(humanPlayers: list[Human], playerCount: int) -> list[Player]:
#     assert(len(humanPlayers) <= playerCount)

#     global numPlayers; numPlayers = playerCount

#     numAgents: int = playerCount - len(humanPlayers)
#     names: list[str] = [name for name in genericNames if name not in [human.name for human in humanPlayers]]
#     names = shuffle(names)

#     return humanPlayers + [Agent(names[i]) for i in range(numAgents)]

genericNames = ["Barbera", "Shaun", "Sandra", "Kim", "Jim", "Lance", "Quinoa", "Prince", "Harry", "Isa", "Dick"]
