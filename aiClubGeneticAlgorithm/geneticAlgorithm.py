from __future__ import division
import random

numberWeAreLookingFor = 140
tolerableError = 0.5
chromosomeSize = 36
populationSize = 500
mutationRate = 0.107
epochs = 250

def encode(x):
  return {
         '0': "0000",
        '1': "0001",
        '2': "0010",
        '3': "0011",
        '4': "0100",
        '5': "0101",
        '6': "0110",
        '7': "0111",
        '8': "1000",
        '9': "1001",
        '+': "1010",
        '-': "1011",
        '*': "1100",
        '/': "1101"  
    }[x]#blank string is the default if not found

def decode(x):
  return {
        "0000": '0',
        "0001": '1',
        "0010": '2',
        "0011": '3',
        "0100": '4',
        "0101": '5',
        "0110": '6',
        "0111": '7',
        "1000": '8',
        "1001": '9',
        "1010": '+',
        "1011": '-',
        "1100": '*',
        "1101": '/',
        "1110": '/',
        "1111": '',
    }[x]#blank string is the default if not found

    #(splitStringEveryNCharacters("gooballooon",2)
    #['go', 'ob', 'al', 'lo', 'oo', 'n']
def chromosomeToMathExpression(chromosome):
  chromosomeTokens = splitStringEveryNCharacters(chromosome,4)
  mathString = ""
  for i in chromosomeTokens:
    mathString +=(nibbleToCharacter(i))
  return cleanupMathExpression(mathString)

def mathExpressionToChromosome(mathString):
  chromosome =""
  for i in mathString:
    chromosome.append(characterToNibble(i))
  return chromosome
  
def nibbleToCharacter(nibble):
  #takes a 4 element string of 1 and 0 and converts it into an ascii char
  character = decode(nibble)
  return character

def characterToNibble(character):
  #takes a char (0-9 +*/-) and converts it to a 4 element binary array
  nibble = encode(character)
  return nibble

      
def generateChromosome():
    return arrayToString(generateRandomArray(chromosomeSize))


def generateChromosomes(numberOfChromosomes):
    chromosomes = []
    for i in range (1,numberOfChromosomes):
        chromosomes.append(generateChromosome())
    return chromosomes 

def generateRandomArray(arraySize):
    returnArray = [];
    for x in range(0, arraySize):
        returnArray.append(str(random.randint(0,1)))
    return returnArray

  
def cleanupMathExpression(mathExpression):
 #if we have a * or / it has to be to the right of a number 
 #no operator can be the last character
  operators = ["*","/","+","-"]
  numbers = ["0","1","2","3","4","5","6","7","8","9"]
  multiplyDivide = ["*","/"]
  newMathExpressionString = ""
  for i in range(0, len(mathExpression)):
        #print("runing this " + str(i) + " times")
        characterPasses = True
        #if this character is an operator
        if mathExpression[i] in operators:
                #if it's the last operator
                if i == len(mathExpression)-1:
                        #print("the last character and is an operator")
                        characterPasses = False
                #if it's a * or / 
                if mathExpression[i] in multiplyDivide:
                #if it's the first character
                        if i == 0:
                              ##  print("it was the first character and multiply divide")
                                characterPasses = False
                #if the character before it is an operator
                        elif mathExpression[i-1] in operators:
                               #### print("this was a +/- and there was an operator before it")
                                characterPasses = False
        if characterPasses:
         # print("it passed")
          newMathExpressionString +=(mathExpression[i])
  return newMathExpressionString

  
      
  
def arrayToString(array):
  return ''.join(array)
  
                            
    #(splitStringEveryNCharacters("gooballooon",2)
    #['go', 'ob', 'al', 'lo', 'oo', 'n']
def splitStringEveryNCharacters(stringToSplit,n):
    return [stringToSplit[i:i+n] for i in range(0, len(stringToSplit), n)]


#Dean's space

def fitnessScore(chromosome):
  mathExpression = chromosomeToMathExpression(chromosome)
  try:
    chromosomeMathValue = eval(mathExpression)
  except:
    return 0.99 
  percentError = abs(( numberWeAreLookingFor - chromosomeMathValue ) / numberWeAreLookingFor)
  return percentError

def createWeightedListOfChromosomes(listOfChromosomes):
    weightedListOfTuples = []
    for chromosome in listOfChromosomes:
        fitness = fitnessScore(chromosome)
        weight = 1/(fitness + 0.000000001)
        weightedListOfTuples.append((weight,chromosome))
    return weightedListOfTuples  
  
def selectTwoToMate(weightedListOfChromosomes):
  pairToMate = []
  for sample in weighted_sample(weightedListOfChromosomes,2):
    pairToMate.append(sample)
  return pairToMate
  
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


def findHighestWeightedChromosome(weightedChromosomes):
    highestWeight = 0
    fittestChromosome = []
    for weight, chromosome in weightedChromosomes:
        if weight > highestWeight:
            highestWeight = weight
            fittestChromosome = chromosome
    return highestWeight, fittestChromosome    

#We should introduce a maximum fitness score.  A score of zero indicates target number hit.

def crossoverChromosomes(chromosomeA, chromosomeB, splitPoint):
  chromosomeAB = chromosomeA[0:splitPoint]+chromosomeB[splitPoint:len(chromosomeB)]
  chromosomeBA = chromosomeB[0:splitPoint]+chromosomeA[splitPoint:len(chromosomeA)]
  
  return mutateChromosome(chromosomeAB,mutationRate), mutateChromosome(chromosomeBA,mutationRate) 

def mutateChromosome(chromosome, mutationRate):
#mutation rate is 0<x<1
  newChromosome =""
  for i in chromosome:
    randomNumber = random.random()
    if randomNumber < mutationRate:
      if chromosome[int(i)]=="1":
          newChromosome+="0"
      else:
          newChromosome+="1"
    else:
        newChromosome+=chromosome[int(i)]
  return newChromosome


decode("0000")

chromosomes = generateChromosomes(populationSize)
for epochNumber in range (0,epochs):
        print("Epoch # " + str(epochNumber))
        nextGenerationChromosomes = []
        weightedChromosomes = createWeightedListOfChromosomes(chromosomes)
        weighting,bestChromosome = findHighestWeightedChromosome(weightedChromosomes)
        mathVersion = chromosomeToMathExpression(bestChromosome)
        print("the best of all the chromosomes was this:")
        print("Weight:" + str(weighting) + " chromosome: "  +  bestChromosome + " mathyversion:" + mathVersion)
        if fitnessScore(bestChromosome) == 0.0:
            print("found the right answer")
            break
        
        while len(nextGenerationChromosomes) < populationSize:
            #print('mayyyyyytinnnnng #' + str(len(nextGenerationChromosomes)))
            pairToMate = selectTwoToMate(weightedChromosomes)
            firstChild,secondChild = crossoverChromosomes(pairToMate[0],pairToMate[1],random.randint(0,10))
            nextGenerationChromosomes.append(firstChild)
            nextGenerationChromosomes.append(secondChild)
        chromosomes = nextGenerationChromosomes
