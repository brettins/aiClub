from __future__ import division
import random
from population import Population
import  generalFunctions

#TODO - Look at research for avoiding local optima  
#http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.106.8662&rep=rep1&type=pdf
# best solutions seem to be randomly generated offspring and 
#variable mutation rate (VMR)  (VMR doesn't actually make it better, 
#but it sets the mutation rate to an optimal value which is 
#apparently hard as balls doing by yourself)


#TODO - our selection process eliminates all parents, which is 
#not ideal - please see Steady-State Selection here:
#http://www.obitko.com/tutorials/genetic-algorithms/selection.php
#elitism (from the same page) also solves a problem we were having where the top few are copied to the next
#generation without a chance of change or mutation - ALPHA DOG STAYS UNTOUCHED



numberWeAreLookingFor = 14044
tolerableError = 0.5
chromosomeSize = 36
populationSize = 1000
mutationRate = 0.107
epochs = 250
geneSize = 4

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
				if not (mathExpression[i] == "*" and mathExpression[i-1] == "*"):
				  characterPasses = False
        if characterPasses:
         # print("it passed")
          newMathExpressionString +=(mathExpression[i])
  return newMathExpressionString

  
      
  
                            
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
  try:
	  percentError =  abs(( numberWeAreLookingFor - chromosomeMathValue ) / numberWeAreLookingFor)
  except:
    	  return 0.99 
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





#chromosomes = generateChromosomes(populationSize)
population  = Population(populationSize,chromosomeSize)
for epochNumber in range (0,epochs):
        print("Epoch # " + str(epochNumber))
        nextGenerationChromosomes = []
        weightedChromosomes = createWeightedListOfChromosomes(population.getPopulation())
        print("got the wegithed chromosomes")
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
            firstChild,secondChild = Population.crossoverChromosomes(pairToMate[0],pairToMate[1],random.randint(0,10),mutationRate,geneSize)
            nextGenerationChromosomes.append(firstChild)
            nextGenerationChromosomes.append(secondChild)
        population.setPopulation(nextGenerationChromosomes)
