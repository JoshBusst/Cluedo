

from random import randint
from typing import Any
from itertools import chain



def isequal(lst1, lst2):
    assert(len(lst1) == len(lst2))

    for i in range(len(lst1)):
        if lst1[i] != lst2[i]:
            return False
    
    return True

def pickrandom(lst: list | dict) -> Any:
    rand: int = randint(0, len(lst) - 1)

    if isinstance(lst, list):
        return lst[rand]
    elif isinstance(lst, dict):
        return lst.values()[rand]
    
def log(value: any) -> None:
    print(f"DEBUG LOG: {str(value)}")

def flatten(matrix: list[list]) -> list:
    return [item for row in matrix for item in row]