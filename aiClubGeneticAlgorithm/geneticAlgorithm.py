from __future__ import division
from population import Population
import random
import numpy
import generalFunctions
import statistics

#TODO
# found a book that has some info on dominant genes, which I think is a great way to efficiently mutate and keep some optimization:
#https://goo.gl/BnC1QJ


#TODO - how do we determine a section of chromosome to be "useful"? For the find a number
#example, if we are trying to get a ridiculously high number, then a section with an expoential 
#shoudl maybe stay pretty similar to get us "up" to the number, and the other parts should vary more
#so we can refine the search. This should apply to other GA problems
#I found another book that talks about this - page 121 here, called a "Messy GA":
#https://www.google.ca/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&cad=rja&uact=8&ved=0CC0QFjABahUKEwjV4I7KiN_GAhWTvIAKHcRlDIE&url=http%3A%2F%2Fwww.boente.eti.br%2Ffuzzy%2Febook-fuzzy-mitchell.pdf&ei=CFWnVdW8KZP5ggTEy7GICA&usg=AFQjCNGfU_i6oWloPS75Dj6Pa216CrB83Q&sig2=68S9EhXvrrS2ItKEhsoRRg&bvm=bv.97949915,d.eXY


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




class GeneticAlgorithm:

    def __init__(self,fitnessFunction):
        self.fitnessFunction = fitnessFunction
        self.populationSize = 1000
        self.numberOfEpochs = 100
        self.chromosomeSize = 36
        self.mutationRate = 1.0/self.chromosomeSize
        self.eliteRatio = 0.005
        self.geneSize = 4
        self.numberOfTimesToMutateElite = 10
        self.acceptableStdDev = 1 
        self.turnsTopWeightHasntChanged = 0
        self.lastTopWeight = 0


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

    def setEliteRatio(self,eliteRatio):
        self.eliteRatio = eliteRatio

    def setChromsomeToHumanReadableFunction(self,chromosomeReadableFunction):
        self.chromosomeReadableFunction = chromosomeReadableFunction

    def run(self):
        population  = Population(self.populationSize,self.chromosomeSize)
        self.adjustedMutationRate = self.mutationRate
        for epochNumber in range (1,self.numberOfEpochs+1):
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
            #if we have a stagnant population, up the mutation rate
            populationIsStagnant= self.isPopulationStagnant(weightedChromosomes,self.acceptableStdDev)
            if  populationIsStagnant or self.turnsTopWeightHasntChanged > 10:
                print("population was stagnant or stuck in local optima increasing mutation rate to "),
                self.adjustedMutationRate += 0.025
                #capped at 50% because more is meaningless as we approach just flipping all the bits
                if self.adjustedMutationRate > .50:
                    self.adjustedMutationRate = .50
                print(self.adjustedMutationRate)
            else :
                self.adjustedMutationRate = self.mutationRate

            weighting,bestChromosome = GeneticAlgorithm.findHighestWeightedChromosome(weightedChromosomes)
            if weighting == self.lastTopWeight:
                self.turnsTopWeightHasntChanged+=1
            else:
                self.lastTopWeight = weighting
            readableVersion = self.chromosomeReadableFunction(bestChromosome)
            print("the best of all the chromosomes was this:")
            print("Weight:" + str(weighting) + " chromosome: "  +  bestChromosome + " readableVersion:" + readableVersion + " value: " + str(eval(readableVersion)))
            if self.fitnessFunction(bestChromosome) == 0.0:
                print("found the right answer")
                break
            numberOfElites = (int)(self.eliteRatio * self.populationSize)
            elites = generalFunctions.takeHighestWeightedItems(weightedChromosomes,numberOfElites)

            nextGenerationChromosomes.extend(x[1] for x in elites)

            for elite in elites:
                for i in range (0,self.numberOfTimesToMutateElite):
                    mutatedElite = Population.mutateChromosome(elite[1],self.adjustedMutationRate)
                    #print("mutatation rate of "),
                    #print(self.adjustedMutationRate)
                    #print("elite looks like this:"),
                    #print(elite[1])
                    #print("mutated elite was")
                    #print(mutatedElite)
                    nextGenerationChromosomes.append(elite[1])

            while len(nextGenerationChromosomes) < self.populationSize:
                #print('mayyyyyytinnnnng #' + str(len(nextGenerationChromosomes)))
                pairToMate = GeneticAlgorithm.selectTwoToMate(weightedChromosomes)
                firstChild,secondChild = Population.crossoverChromosomes(pairToMate[0],pairToMate[1],random.randint(0,10),self.adjustedMutationRate,self.geneSize)
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

    def isPopulationStagnant(self,weightedChromosomes,acceptableStdDev):
        weights = []
        for weight, chromosome in weightedChromosomes:
            weights.append(weight)
        standardDeviationOfWeights = statistics.stdev(weights)
        meanOfWeights = statistics.mean(weights)
        normalizedStandardDeviation = standardDeviationOfWeights / meanOfWeights
        print("population had a normalized stdev of "), 
        print(normalizedStandardDeviation)

        #if we have a higher standard deviation than acceptable, we are not stagant!
        if normalizedStandardDeviation > acceptableStdDev:
            return False
        #lower stddev than acceptable, this is a stagnant population
        else:
            return True
