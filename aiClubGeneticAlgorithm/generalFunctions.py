import random

def generateRandomArray(arraySize):
    returnArray = [];
    for x in range(0, arraySize):
        returnArray.append(str(random.randint(0,1)))
    return returnArray

def arrayToString(array):
    return ''.join(array)
