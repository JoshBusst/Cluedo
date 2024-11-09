


def isequal(lst1, lst2):
    assert(len(lst1) == len(lst2))

    for i in range(len(lst1)):
        if lst1[i] != lst2[i]:
            return False
    
    return True

def pickrandom(lst):
    from random import randint

    rand = randint(0, len(lst) - 1)

    if isinstance(lst, list):
        return lst[rand]
    elif isinstance(lst, dict):
        return lst.values()[rand]
    
