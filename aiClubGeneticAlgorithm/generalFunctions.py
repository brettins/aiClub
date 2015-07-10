import random

def generateRandomArray(arraySize,minimum,maximum):
    returnArray = [];
    for x in range(0, arraySize):
        returnArray.append(str(random.randint(minimum,maximum)))
    return returnArray

def arrayToString(array):
    return ''.join(array)

def weighted_sample(items, n):
    total = float(sum(w for w, v in items))
    i = 0
    w, v = items[0]
    while n:
        x = total * (1 - random.random() ** (1.0 / n))
        total -= x
        while x > w:
            x -= w
            i += 1
            w, v = items[i]
        w -= x
        yield v
        n -= 1

def splitStringEveryNCharacters(stringToSplit,n):
    """
    Usage: (splitStringEveryNCharacters("gooballooon",2)
    ['go', 'ob', 'al', 'lo', 'oo', 'n']
    """
    return [stringToSplit[i:i+n] for i in range(0, len(stringToSplit), n)]
