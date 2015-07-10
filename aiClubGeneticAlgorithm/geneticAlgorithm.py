from __future__ import division
from population import Population
import random
import generalFunctions

class GeneticAlgorithm:

    def __init__(self,fitnessFunction):
        self.fitnessFunction = fitnessFunction
        self.populationSize = 1000
        self.numberOfEpochs = 100
        self.mutationRate = 0.107
        self.chromosomeSize = 36
        self.geneSize = 4

    def setGeneSize(self,geneSize):
        self.geneSize = geneSize

    def setPopulationSize(self,populationSize):
        self.populationSize = populationSize

    def setNumberOfEpochs(self,numberOfEpochs):
        self.numberOfEpochs = numberOfEpochs
    
    def setMutationRate(self,mutationRate):
        self.mutationRate = mutationRate

    def setChromosomeSize(self,chromosomeSize):
        self.chromosomeSize = chromosomeSize

    def setChromsomeToHumanReadableFunction(self,chromosomeReadableFunction):
        self.chromosomeReadableFunction = chromosomeReadableFunction

    def run(self):
        population  = Population(self.populationSize,self.chromosomeSize)
        for epochNumber in range (0,self.numberOfEpochs):
            print("Epoch # " + str(epochNumber))
            nextGenerationChromosomes = []
            weightedChromosomes,foundSolution = self.createWeightedListOfChromosomes(population.getPopulation())
            if foundSolution:
                print("")
                print("")
                print("")
                print("")
                print("**********************")
                print("Found the right answer")
                print("**********************")
                print("Chromosome: ")
                print( weightedChromosomes[1])
                print( "Readable version:")
                print(self.chromosomeReadableFunction(weightedChromosomes[1]))
                break
            weighting,bestChromosome = GeneticAlgorithm.findHighestWeightedChromosome(weightedChromosomes)
            readableVersion = self.chromosomeReadableFunction(bestChromosome)
            print("the best of all the chromosomes was this:")
            print("Weight:" + str(weighting) + " chromosome: "  +  bestChromosome + " readableVersion:" + readableVersion + " value: " + str(eval(readableVersion)))
            if self.fitnessFunction(bestChromosome) == 0.0:
                print("found the right answer")
                break
            numberOfElites = (int)(0.01 * self.populationSize)
            elites = generalFunctions.takeHighestWeightedItems(weightedChromosomes,numberOfElites)

            nextGenerationChromosomes.extend(x[1] for x in elites)

            while len(nextGenerationChromosomes) < self.populationSize:
                #print('mayyyyyytinnnnng #' + str(len(nextGenerationChromosomes)))
                pairToMate = GeneticAlgorithm.selectTwoToMate(weightedChromosomes)
                firstChild,secondChild = Population.crossoverChromosomes(pairToMate[0],pairToMate[1],random.randint(0,10),self.mutationRate,self.geneSize)
                nextGenerationChromosomes.append(firstChild)
                nextGenerationChromosomes.append(secondChild)
            population.setPopulation(nextGenerationChromosomes)
        


    @staticmethod
    def findHighestWeightedChromosome(weightedChromosomes):
        highestWeight = 0
        fittestChromosome = []
        for weight, chromosome in weightedChromosomes:
            if weight > highestWeight:
                highestWeight = weight
                fittestChromosome = chromosome
        return highestWeight, fittestChromosome    

    @staticmethod
    def selectTwoToMate(weightedListOfChromosomes):
        pairToMate = []
        for sample in generalFunctions.weighted_sample(weightedListOfChromosomes,2):
            pairToMate.append(sample)
        return pairToMate

    def createWeightedListOfChromosomes(self,listOfChromosomes):
        weightedListOfTuples = []
        for chromosome in listOfChromosomes:
            fitness = self.fitnessFunction(chromosome)
            if not fitness is None:
                if not fitness == 0:
                    weight = 1/(fitness)
                    weightedListOfTuples.append((weight,chromosome))
                else:
                    return (0,chromosome),True


        return weightedListOfTuples, False 
