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

def weightedSampleNoRepeat(originalItems, n):
    items = list(originalItems)
    total = float(sum(w for w, v in items))
    i = 0
    w, v = items[0]

    if n > 0:
        x = total * (1 - random.random() ** (1.0 / n))
        total -= x
        while x > w:
            x -= w
            i += 1
            w, v = items[i]
        w -= x
        items.pop(i)
        if n == 1:
            return v
        return [v] + [weightedSampleNoRepeat(items,n-1)]


def takeHighestWeightedItems(items, n):
    sortedItems = sorted(items,reverse=True)
    itemsToReturn = []
    for i in range(0,n):
        itemsToReturn.append(sortedItems[i])
    return itemsToReturn


def splitStringEveryNCharacters(stringToSplit,n):
    """
    Usage: (splitStringEveryNCharacters("gooballooon",2)
    ['go', 'ob', 'al', 'lo', 'oo', 'n']
    """
    return [stringToSplit[i:i+n] for i in range(0, len(stringToSplit), n)]


  
#taken from PyEvolve library
def listSwapElement(lst, indexa, indexb):
    """ Swaps elements A and B in a list.

    Example:
       >>> l = [1, 2, 3]
       >>> Util.listSwapElement(l, 1, 2)
       >>> l
       [1, 3, 2]

    :param lst: the list
    :param indexa: the swap element A
    :param indexb: the swap element B
    :rtype: None

    """
    temp = lst[indexa]
    lst[indexa] = lst[indexb]
    lst[indexb] = temp

