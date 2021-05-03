import numpy
import operator
from GeneticProgrammingLibrary import Rule
from CommonLibrary import CommonMethods as cm

class GeneticProgram():

    # Defining the population size.
    sol_per_pop = 5
    # Number of terms in our rule
    num_atomic_rules = 3
    # The population will have sol_per_pop chromosomes where each chromosome has num_atomic_rules genes.
    pop_size = (sol_per_pop, num_atomic_rules)
    # The list containing failed rules
    failed_rules = []


    def __init__(self, ruleNumber, numGenerations, trainingSet):
        self.ruleNumber = ruleNumber
        #the training set
        self.trainingSet = trainingSet
        #defines the number of rounds we will have when running our program
        self.numGenerations = numGenerations
        # contains the current set of solutions for this rule
        self.current_population = [None]*self.sol_per_pop

        #define an initial population of rules for our genetic program
        for i in range(0, self.sol_per_pop):
            self.current_population[i] = Rule.Rule(self.ruleNumber)

    # Return the parent in the list with the best classification score
    def get_max_parent(self, current_solutions):
        currentMax = current_solutions[0]

        for solution in current_solutions:
            if (solution.fitness['ClassificationOfTargetHand'] > currentMax.fitness['ClassificationOfTargetHand']):
                currentMax = solution
            # if they are equal we check if the classification of other hands is betterge
            elif (solution.fitness['ClassificationOfTargetHand'] == currentMax.fitness['ClassificationOfTargetHand']):
                if (solution.fitness['ClassificationOfOtherHands'] > currentMax.fitness['ClassificationOfOtherHands']):
                    currentMax = solution
        return currentMax

    # Choose from the current set of solutions, the best two solutions and return them
    def select_mating_pool(self):
        # Selecting the best 2 individuals in the current generation as parents for producing the offspring of the next generation.
        # 0th index is reserved for the best solution, 1st index is second best solution
        current_solutions = self.current_population[:]
        parent_list = [ None, None ]

        parent_list[0] = self.get_max_parent(current_solutions)
        current_solutions.remove(parent_list[0])

        parent_list[1] = self.get_max_parent(current_solutions)

        # ensure they are not the same rule (we are guaranteed to have at least one different rule)
            # The guarantee is due to the mutation, crossover and randomly generated rule
        while (parent_list[0].compareRules(parent_list[1])):
            current_solutions.remove(parent_list[1])
            parent_list[1] = self.get_max_parent(current_solutions)

        return parent_list

    # generates the next generation from the parent list (retrived by calling the select_mating_pool() method)
    # places in the next generation the best solution, the second best solution, crossover between best and second best solution, mutation of best solution
    # and a randomly generated new solution
    def create_next_generation(self, parent_list):

        # If our best solution has gotten us nothing, then we restart
        if(parent_list[0].fitness['ClassificationOfTargetHand'] == 0):
            for i in range(0, self.sol_per_pop):
                self.current_population[i] = Rule.Rule(self.ruleNumber)
            return

        #Given two parents we create the next generation
        # We have 3 operations that we perform to achieve the next generation
        # First we have a crossover between our best two solutions
        # Second we have a mutation of our best solution
        # Third we define a new solution at random

        crossover_solution = parent_list[0].crossover(parent_list[1])
        mutation_solution = parent_list[0].mutation()

        self.current_population =   [
                                        parent_list[0], 
                                        parent_list[1], 
                                        crossover_solution, 
                                        mutation_solution, 
                                        Rule.Rule(self.ruleNumber)
                                    ]
        


    """
        This method is used to calculate the fitness (accuracy) of the current rule. 
        Each rule is tested on the number of samples it classifies correctly in one of two categories.
            1. Those that are in the set of samples that belong to the target hand we are aiming to classify.
            2. Those that are in the set of samples that belong to the target hands we are not aiming to classify (all other hands).
        The fitness is then calculated as the number of correct classifications for each set over the total number of instances of each set.
    """
    def calculateFitness(self):
        #test each hand on each of our current population of rules
        target_hand_correct = [0]*self.sol_per_pop
        other_hand_correct = [0]*self.sol_per_pop
        count_target_hand = 0
        count_other_hand = 0

        #loop for each hand in the training set
        for i in range(0, len(self.trainingSet)):
            hand = self.trainingSet.iloc[i]
            #get the hand and separate it
            suits, ranks, handValue = cm.separateRankAndSuit(hand)

            #increment for each type of hand this is classifying (target hand or other)
            if (handValue == self.ruleNumber):
                count_target_hand += 1
            else:
                count_other_hand += 1

            #loop for each rule in the currentPopulation
            for i in range(0, self.sol_per_pop):
                #If we get the right answer for this particular hand, increment the fitness value of this solution
                expressionVal = self.current_population[i].testFitness(suits, ranks, handValue)
                if (expressionVal and handValue == self.ruleNumber):
                    target_hand_correct[i] += 1
                elif (not expressionVal and handValue != self.ruleNumber):
                    other_hand_correct[i] += 1
                    
        for i in range(0, self.sol_per_pop):

            #avoid divisions by zero
            if (target_hand_correct[i] != 0):
                target_hand_correct[i] = target_hand_correct[i] / count_target_hand
            
            if (other_hand_correct[i] != 0):
                other_hand_correct[i] = other_hand_correct[i] / count_other_hand

            self.current_population[i].fitness =    {
                                                        'ClassificationOfTargetHand': target_hand_correct[i],
                                                        'ClassificationOfOtherHands': other_hand_correct[i]
                                                    }

    # This method runs the genetic program for a rule.
    def runProgram(self):

        # Run this program for the specified number of generations
        for i in range(0, self.numGenerations):
            # calculate the fitness of the current generation
            self.calculateFitness()

            # print out the current generation
            print("Generation ", i, ": ")
            for solution in self.current_population:
                print()
                print(solution.fitness)
                print(solution.rule)
            print()
            print()
            print()

            # Assign the current population the value of the next generation and reiterate
            if (i != self.numGenerations - 1):
                print("Defining next generation")
                # select the mating pool for the next generation from our list of current rules
                parent_list = self.select_mating_pool()
                # create the next generation from the parent list we have created
                self.create_next_generation(parent_list)
                print("Done defining next generation")
        
        print("The Final Solution: ")
        for solution in self.current_population:
                print()
                print(solution.fitness)
                print(solution.rule)
        print()
        print()
        print()

        print("done")

    # Returns the classification of the hand based on the hierarchy of extracted rules.
    # (Note: The rules have been manually extracted from the output of the genetic program.
    def classifyHand(self, ranks, suits):
        if (True and cm.numZeros(suits) == 4 and not cm.separationOfZeros(suits)):
            return 9
        elif (True and cm.numZeros(suits) == 4 and cm.elemsAscDesc(ranks, isRank=True)):
            return 8
        elif (cm.numZeros(ranks) == 3 and cm.separationOfZeros(ranks) and not cm.separationOfZeros(suits)):
            return 6
        elif (cm.numZeros(ranks) == 3 and True and True):
            return 7
        elif (True and cm.numZeros(suits) == 4 and not cm.separationOfZeros(suits)):
            return 5
        elif (True and True and cm.elemsAscDesc(ranks, isRank=True)):
            return 4
        elif (cm.numZeros(ranks) == 2 and cm.separationOfZeros(ranks) and not cm.separationOfZeros(suits)):
            return 2
        elif (cm.numZeros(ranks) == 2 and True and True):
            return 3
        elif (cm.numZeros(ranks) == 1 and not cm.separationOfZeros(ranks) and True):
            return 1
        else:
            return 0

    # This method returns the integer value of the hand based on the hierarchy we have constructed from the extracted rules.
    # Input: The set of hands in the test set and the tags for those hands.
    # Ouput: The total number of correctly classified hands over the total number of hands in the test set.
    def classifyHandGP(self, test_hands, test_tags):
        print("here")
        total_correct = 0
        for i in range(0, len(test_hands)):
            hand = test_hands.iloc[i]
            tag = test_tags[i]
            # hand value will be -1
            suits, ranks, handValue = cm.separateRankAndSuit(hand, False)
            # classify the hand using our extracted rules
            classification = self.classifyHand(ranks, suits)

            if (classification == tag):
                total_correct += 1


        print("Correctly classified %s total test examples out of %s examples" %(total_correct, len(test_tags)) )
        