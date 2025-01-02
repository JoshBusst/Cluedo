from abc import abstractmethod
from cards import *
from console import *

from random import shuffle



class Player:
    def __init__(self, name: str, ishuman: bool):
        self.name: str = name
        self.hand: list = []
        self.ishuman: bool = ishuman

    @abstractmethod
    def seeCard(self, card: str, playerName: str) -> None:
        pass

    @abstractmethod
    def getRumour(self) -> dict[str,str]:
        pass

    @abstractmethod
    def getAccusation(self) -> dict[str,str]:
        pass

    def turn(self) -> int:
        pass

    def setHand(self, hand: list[str]) -> None:
        self.hand = hand

    def hasCards(self, rumour: dict[str,str]) -> bool:
        return any([card in self.hand for card in rumour.values()])
        
    def hasCard(self, card: str) -> bool:
        return card in self.hand
        
    def printHand(self) -> None:
        consoleOut(f"{self.name}'s hand: {self.hand}")



class Agent(Player):
    def __init__(self, name: str):
        Player.__init__(self, name, False)
        
        self.tracker: Tracker = Tracker()

    def recordCard(self, playername: str, card: str) -> None:
        self.tracker.addCard(playername, card)

    def recordPass(self, playername: str, rumour: dict) -> None:
        self.tracker.addAntiCards(playername, rumour.values())
        
    def recordShow(self, player1name: str, player2name: str, rumour: dict) -> None:
        pass
        # self.tracker.addAntiCards(playername, rumour.values())
        
    def turn(self) -> int:
        pass




class Human(Player):
    def __init__(self, name: str):
        Player.__init__(self, name, True)

    def seeCard(self, playerName: str, card: str):
        consoleOut(f"{playerName} shows you the card {card}")

    def getRumour(self) -> dict[str, str]:
        person = self.getInput(cardDict['people'],
                               "Please input a persons name.",
                               f"*Please select a valid player name from: {cardDict['people']}.")
        
        room = self.getInput(cardDict['rooms'],
                               "Please input a room.",
                               f"*Please select a valid room from: {cardDict['rooms']}")

        weapon = self.getInput(cardDict['weapons'],
                               "Please input a murder weapon.",
                               f"*Please select a valid weapon from: {cardDict['weapons']}")
        
        return {'people': person, 'rooms': room, 'weapons': weapon}

    def getAccusation(self) -> dict[str, str]:
        return self.getRumour()

    def turn(self) -> None:
        choice: str = self.getInput(['a','r'], "Would you like to accuse or start a rumour? a/r", "Please select a or r...")
        
        return choice
    
    def getInput(self, validInputs: list[str], startMsg: str, errorMsg: str) -> str:
        consoleOut(startMsg)
        data: str = input(">_ ").lower()

        while data not in validInputs:
            consoleOut(errorMsg)
            data = input(">_ ").lower()

        return data


# populates empty player spaces with agents and sets global variables. Returns a list of Player of size playerCount
# def loadPlayers(humanPlayers: list[Human], playerCount: int) -> list[Player]:
#     assert(len(humanPlayers) <= playerCount)

#     global numPlayers; numPlayers = playerCount

#     numAgents: int = playerCount - len(humanPlayers)
#     names: list[str] = [name for name in genericNames if name not in [human.name for human in humanPlayers]]
#     names = shuffle(names)

#     return humanPlayers + [Agent(names[i]) for i in range(numAgents)]

genericNames = ['John','Barbera','Jessie','Jack','Chloe','Casey','Emily','Josh','Corey','Georgia','Stacey','Harry','Paul','Shaun']
