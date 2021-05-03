import random
from CommonLibrary import CommonMethods as cm

"""
    This class defines a rule associated with a specific hand 0-9.
    A rule is comprised of various atomic rules as defined in the atomicRules array.
    An atomic rule is a feature that has been deemed interesting through feature engineering.
    We build our rule out of these features and allow for operations such as mutation and crossover
    between two rules.
"""
class Rule():

    # This is our list of features that we will use to define the rule
    # Common between all classes of rules
    atomicRules =   [ 
                        ['True', 'cm.numZeros(ranks) == 1', 'cm.numZeros(ranks) == 2', 'cm.numZeros(ranks) == 3', 'cm.numZeros(ranks) == 4', 'cm.acePresent(ranks)'],
                        ['True', 'cm.separationOfZeros(ranks)', 'not cm.separationOfZeros(ranks)', 'cm.numZeros(suits) == 4'],
                        ['True', 'cm.elemsAscDesc(ranks, isRank=True)', 'cm.separationOfZeros(suits)', 'not cm.separationOfZeros(suits)']
                    ]
      

    def __init__(self, ruleNumber):
        #The number of our rule, initially set to -1
        self.ruleNumber = ruleNumber

        # This variable holds the fitness value of this rule. It is a decimal value out of 1.
        # The value is given by the (number of correct classifications / values in training set)
        self.fitness =  {    
                            'ClassificationOfTargetHand': 0,
                            'ClassificationOfOtherHands': 0
                        }

        # array holding our atomic rules
        self.atoms = []
        # ensure that our atoms are not a tautology nor a contradiction
        while (not self.isValidRule()):
            self.atoms =    [
                                random.choice(self.atomicRules[0]),
                                random.choice(self.atomicRules[1]),
                                random.choice(self.atomicRules[2])
                            ]


        #create our rule out of the atomic variables
        self.rule = '%s and %s and %s' %(self.atoms[0], self.atoms[1], self.atoms[2])

    """
        Here we perform a crossover operation between two rules. We take the atomic rules x1-x2 from the second
        version of the rule and we place them in the same place as the first version of the rule.
    """
    def crossover(self, crossoverRule):
        new_atoms = [
                        self.atoms[0],
                        crossoverRule.atoms[1],
                        crossoverRule.atoms[2]
                    ]

        #redefine the rule after modifying the atomic variables
        new_rule = '%s and %s and %s' %(new_atoms[0], new_atoms[1], new_atoms[2])

        new_solution = Rule(self.ruleNumber)
        new_solution.atoms = new_atoms
        new_solution.rule = new_rule

        # If we happen upon a tautology when performing a crossover then we must mutate it
        if (not new_solution.isValidRule()):
            return new_solution.mutation()

        return new_solution

    """
        Here we modify a rule through mutation. This involves a single rule and the operation is performed
        on itself. The operation involves choosing a variable x1-x5 at random and reassigning it a new
        atomic rule that is not equal to its current atomic rule.
    """
    def mutation(self):
        # need a deep copy of this list
        new_atoms = self.atoms[:]
        #pick a variable at random to redefine
        index = random.randint(0,2)
        #pick the atomic rule that we are going to redefine it with, also at random
        newAtomicRule = random.choice(self.atomicRules[index])

        #make sure the new rule is different than the last and that it is not a tautology
        while (new_atoms[index] == newAtomicRule and (not self.isValidRule(new_atoms)) ):
            newAtomicRule = random.choice(self.atomicRules[index])

        #reassign the variable that we have chosen with the value of the new atomic rule
        new_atoms[index] = newAtomicRule

        #redefine the rule after modifying the atomic variables
        new_rule = '%s and %s and %s' %(new_atoms[0], new_atoms[1], new_atoms[2])

        new_solution = Rule(self.ruleNumber)
        new_solution.atoms = new_atoms
        new_solution.rule = new_rule


        return new_solution
        
    # Compare two rules to see if they are the same by comparing their atoms
    def compareRules(self, rule_to_compare):
        if (sorted(self.atoms) == sorted(rule_to_compare.atoms)):
            return True
        return False

    # Check whether a rule is valid by ensuring that not all atoms in the rule are True.
    def isValidRule(self, atoms = None):
        if (atoms):
            for atom in atoms:
                if (atom != 'True'):
                    return True
            return False

        for atom in self.atoms:
            if (atom != 'True'):
                return True
        return False


    #This method evaluates the rule given a hand split into suits and ranks and the handValue
    def testFitness(self, suits, ranks, handValue):
        return eval(self.rule)