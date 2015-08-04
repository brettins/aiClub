from __future__ import division
import random
import generalFunctions
from simpleeval import simple_eval
from geneticAlgorithm import GeneticAlgorithm




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
  chromosomeTokens = generalFunctions.splitStringEveryNCharacters(chromosome,4)
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

  
      
  
                            


#Dean's space

def fitnessScore(chromosome):
  mathExpression = chromosomeToMathExpression(chromosome)
  try:
    chromosomeMathValue = simple_eval(mathExpression)
  except:
    return None
  try:
	  percentError =  abs(( numberWeAreLookingFor - chromosomeMathValue ) / numberWeAreLookingFor)
  except:
    	  return None
  return percentError

  

#We should introduce a maximum fitness score.  A score of zero indicates target number hit.

numberWeAreLookingFor = int(raw_input('Enter a number to look for:'))
tolerableError = 0.5
chromosomeSize = 400 
populationSize = 1000
epochs = 250

simple_eval.POWER_MAX = 10000

geneticAlgorithm = GeneticAlgorithm(fitnessScore)
geneticAlgorithm.setPopulationSize(populationSize)
geneticAlgorithm.setNumberOfEpochs(epochs)
geneticAlgorithm.setChromosomeSize(chromosomeSize)
geneticAlgorithm.setChromsomeToHumanReadableFunction(chromosomeToMathExpression)
geneticAlgorithm.setGeneSize(4)

#mutationRate = 0.02
#geneticAlgorithm.setMutationRate(mutationRate)

geneticAlgorithm.run()
print('we were looking for ')
print(numberWeAreLookingFor)
