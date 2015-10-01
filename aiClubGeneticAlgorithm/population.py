import generalFunctions
import random
import math

class Population:
            
    def __init__(self,numberOfChromosomes,lengthOfChromosomes):
        """Randomly generates a population of chromosome and stores it in a class variable"""
        self.populationSize     = numberOfChromosomes
        self.chromosomeLength   = lengthOfChromosomes
        self.population         = self.generateChromosomes(self.populationSize,self.chromosomeLength)

    def generateChromosome(self,length):
        """Generates one chromsome as a random series of 0s and 1s"""
        return generalFunctions.arrayToString(generalFunctions.generateRandomArray(length,0,1))


    def generateChromosomes(self, numberOfChromosomes,length):
        """Generates a list of randomly generated chromosomes and return that list"""
        chromosomes = []
        for i in range (1,numberOfChromosomes):
            chromosomes.append(self.generateChromosome(length))
        return chromosomes 

    def getPopulation(self):
        """Get the population and return it (list)"""
        return self.population

    def setPopulation(self,newPopulation):
        """Overwrite the current population with a new population (list)"""
        self.population = newPopulation

    @staticmethod
    def crossoverChromosomes(chromosomeA, chromosomeB, mutationRate,geneSize):
        #splitPoint = (splitPoint%(len(chromosomeA)/geneSize))*geneSize
        sister,brother = Population.twoPointCrossover(chromosomeB,chromosomeA)
        return Population.mutateChromosome(sister,mutationRate), Population.mutateChromosome(brother,mutationRate) 

    @staticmethod
    def invokeWrathOfGodCatastrophe(population):
        sizeAfterCatastrophe = int((len(population) * 0.10))
        print(sizeAfterCatastrophe)
        return  random.sample(population,sizeAfterCatastrophe)

    #taken from PyEvolve
    @staticmethod
    def twoPointCrossover(mom,dad):
       """ The 1D Binary String crossover, Two Point

       .. warning:: You can't use this crossover method for binary strings with length of 1.

       """
       sister = None
       brother = None
       gMom = mom
       gDad = dad
       

       cuts = [random.randint(1, len(gMom)-1), random.randint(1, len(gMom)-1)]

       if cuts[0] > cuts[1]:
          generalFunctions.listSwapElement(cuts, 0, 1)

       sister =  gMom[0:cuts[0]] + gDad[cuts[0]:cuts[1] ] + gMom[cuts[1]:]
       brother = gDad[0:cuts[0]]  + gMom[cuts[0]:cuts[1]] + gDad[cuts[1]:]

       return (sister, brother)


    @staticmethod
    def mutateChromosome(chromosome, mutationRate):
        '''
        print("")
        print("#### MUTATION TIME ######:")
        print("item to mutate looks like this:")
        print(chromosome)
        print("mutatation rate of "),
        print(mutationRate)
        '''
        #mutation rate is 0<x<1
        newChromosome =""
        numberOfMutations = 0
        for i in chromosome:
            randomNumber = random.random()
            if randomNumber < mutationRate:
                numberOfMutations +=1
                if i=="1":
                    newChromosome+="0"
                else:
                    newChromosome+="1"
            else:
                newChromosome+=i
        '''
        print("mutated item looks like this: ")
        print(newChromosome)
        print("with"),
        print(numberOfMutations),
        print("mutations.")
        '''
        return newChromosome
