
def AND(elements):
    if all(elements):
        return 1
    else:
        return 0


def NAND(elements):
    if all(elements):
        return 0
    else:
        return 1


def OR(elements):
    if any(elements):
        return 1
    else:
        return 0


def XOR(elementA, elementB):
    if elementA != elementB:
        return 1
    else:
        return 0


def INVERTER(element):
    return not element


def NOR(elements):
    if any(elements):
        return 0
    else:
        return 1


def XNOR(elementA, elementB):
    if elementA == elementB:
        return 1
    else:
        return 0
