from cards import *
from players import *
from console import *
from lib import *
from random import shuffle
from copy import copy



class Event:
    def __init__(self, playername: str='', rumour: dict[str,str]={}):
        self.playername = playername
        self.rumour: dict[str,str] = rumour
        self.passes: list[str] = []
        self.whoShowed: str = None

    def print(self):
        print(f" >>: {formatRumour()}")
        print(f" > Passes: {self.passes}")
        print(f" > Who showed: {self.whoShowed}")

    def rumourCards(self):
        return list(self.rumour.values())
    
class Events:
    def __init__(self):
        self.history: list[Event] = []
        self.len: int = 0

    def addRumour(self, playername, rumour):
        event = Event(playername, rumour)

        self.history.append(event)
        self.len += 1

    def addPass(self, playername):
        self.history[-1].passes.append(playername)

    def addAccusation(self, playername: str, accusation: dict[str, str]):
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



def dealcards(players: list[Player]) -> list[str]:
    cards = copy(RAWCARDS)
    shuffle(cards)

    # categorise shuffled list and take first entry of each category
    centreCardsdict = categorise(cards)
    centreCards = [lst[0] for lst in centreCardsdict.values()]

    # remove three centre cards from dealable cards
    cards = [card for card in cards if card not in centreCards]


    numPlayers = len(players)
    deal = [[] for _ in range(numPlayers)]

    for i, card in enumerate(cards):
        deal[i % numPlayers].append(card)

    for i, hand in enumerate(deal):
        players[i].setHand(hand)

    return centreCards

def removePlayer(playerName: str) -> None:
    global players, numPlayers

    players = [player for player in players if player.name != playerName]
    numPlayers = len(players)

# def accuse(name: str, accusation: dict[str,str]):
#     consoleOut("%s accuses %s in the %s with the %s!" %(name, *accusation.values()), '>!')

#     if isequal(list(accusation.values()), centreCards):
#         global gameover

#         consoleOut(f"{name} wins the game!", '>#')
#         gameover = True
#     else:
#         consoleOut(f"{name} has been murdered!", '>!')
#         events.addAccusation(name, accusation)

#         # player is removed from the game
#         global players, numPlayers, turn
#         players = [player for player in players if player.name != name]
#         numPlayers -= 1
#         turn -= 1

def startRumour(currentPlayer: Player):
    rumour: dict[str,str] = currentPlayer.getRumour()
    printRumour(currentPlayer.name, rumour)
    events.addRumour(currentPlayer.name, rumour)

    for playerAsked in otherPlayers(turn):
        if playerAsked.hasCards(rumour):
            currentPlayer.seeCard(playerAsked.name, playerAsked.showCard(currentPlayer.name, rumour))
            publiciseShow(playerAsked.name, currentPlayer.name, rumour)
            events.addShow(playerAsked.name)
            break
        else:
            publicisePass(playerAsked.name, rumour)
            events.addPass(playerAsked.name)

def makeAccusation(currentPlayer: Player):
    accusation: dict[str,str] = currentPlayer.getAccusation()
    printAccusation(currentPlayer.name, accusation)

    events.addAccusation(currentPlayer.name, accusation)

    if isequal(centreCards, list(accusation.values())):
        consoleOut(f"\n{currentPlayer.name} is the winner!!!\n")
        exit()
    else:
        consoleOut(f"\n{currentPlayer.name} has been murdered!")
        removePlayer(currentPlayer.name)



def publicisePass(playerName: str, currentRumour: dict[str, list]) -> None:
    consoleOut(f"{playerName} passes.")

    for player in otherPlayers(turn):
        if not player.ishuman:
            player.recordPass(playerName, currentRumour)

def publiciseShow(showerName: str, seerName: str, currentRumour: dict[str, list]) -> None:
    consoleOut(f"{showerName} shows {seerName} a card.")

    for player in otherPlayers(turn):
        if not player.ishuman:
            player.recordShow(showerName, seerName, currentRumour)

def nextTurn() -> int:
    return (turn + 1) % numPlayers

def otherPlayers(index: int) -> list[Player]:
    # order of appearance is essential here
    return players[index+1:] + players[:index]
    # return [players[(i + index) % numPlayers] for i in range(numPlayers - 1)]
    


players: list[Player] = [] #[Human("Josh")]
events = Events()
numPlayers: int = 4

for i in range(numPlayers):
    players.append(Agent(genericNames[i]))

centreCards: list[str] = dealcards(players)

gameover: bool = False
turn: int = 0
i = 0


if __name__ == "__main__":
    while not gameover and i < 100:
        i += 1

        currentPlayer = players[turn]
        consoleOut(f"\n> It's {currentPlayer.name}'s turn!")


        action = currentPlayer.turn()

        if action == 'r': # start rumour
            consoleOut(f"{currentPlayer.name} starts a rumour.")
            startRumour(currentPlayer)

        elif action == 'a': # accuse
            consoleOut(f"{currentPlayer.name} makes an accusation!")
            makeAccusation(currentPlayer)

        else:
            consoleOut(f"{currentPlayer.name} is confused. No action taken.")
            log(action)


        turn = nextTurn()

        if len(players) == 1:
            consoleOut("># %s wins the game! By default :/\n It was %s in the %s with the %s." %(players[0].name, *centreCards))
            exit()

        elif len(players) <= 0:
            gameover = True

    consoleOut(f"-- Turns taken: {i}")