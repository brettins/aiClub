import generalFunctions
import random

class Population:
            
    def __init__(self,numberOfChromosomes,lengthOfChromosomes):
        self.populationSize     = numberOfChromosomes
        self.chromosomeLength   = lengthOfChromosomes
        self.population         = self.generateChromosomes(self.populationSize,self.chromosomeLength)

    def generateChromosome(self,length):
        return generalFunctions.arrayToString(generalFunctions.generateRandomArray(length))


    def generateChromosomes(self, numberOfChromosomes,length):
        chromosomes = []
        for i in range (1,numberOfChromosomes):
            chromosomes.append(self.generateChromosome(length))
        return chromosomes 

    def getPopulation(self):
        return self.population

    def setPopulation(self,newPopulation):
        self.population = newPopulation

    @staticmethod
    def crossoverChromosomes(chromosomeA, chromosomeB, splitPoint,mutationRate):
        chromosomeAB = chromosomeA[0:splitPoint]+chromosomeB[splitPoint:len(chromosomeB)]
        chromosomeBA = chromosomeB[0:splitPoint]+chromosomeA[splitPoint:len(chromosomeA)]
        return Population.mutateChromosome(chromosomeAB,mutationRate), Population.mutateChromosome(chromosomeBA,mutationRate) 

    @staticmethod
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
