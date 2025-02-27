
VERBOSE: bool = True



def formatRumour(playername: str, rumour: dict[str,str]) -> str:
    return "%s thinks it was %s in the %s with the %s." %(playername, *rumour.values())

def formatAccusation(playername: str, accusation: dict[str,str]) -> str:
    return "%s accuses %s in the %s with the %s!" %(playername, *accusation.values())
  
def consoleOut(msg: str) -> None:
    if not VERBOSE: return
    print(f"{msg}")

def printRumour(playerName: str, rumour: dict) -> None:
    consoleOut('>>: %s' %formatRumour(playerName, rumour))

def printAccusation(playerName: str, rumour: dict) -> None:
    consoleOut('>>! %s' %formatAccusation(playerName, rumour))

def getUserInput(validInputs: list[str], startMsg: str, errorMsg: str='') -> str:
    if errorMsg == '': errorMsg = f"*Please select a valid option from {validInputs}."
    
    consoleOut(startMsg)
    data: str = input(">_ ").lower()

    while data not in validInputs:
        consoleOut(errorMsg)
        data = input(">_ ").lower()

    return data



