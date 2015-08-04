import generalFunctions
import random

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
    def crossoverChromosomes(chromosomeA, chromosomeB, splitPoint,mutationRate,geneSize):
        splitPoint = (splitPoint%(len(chromosomeA)/geneSize))*geneSize
        chromosomeAB = chromosomeA[0:splitPoint]+chromosomeB[splitPoint:len(chromosomeB)]
        chromosomeBA = chromosomeB[0:splitPoint]+chromosomeA[splitPoint:len(chromosomeA)]
        return Population.mutateChromosome(chromosomeAB,mutationRate), Population.mutateChromosome(chromosomeBA,mutationRate) 

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
