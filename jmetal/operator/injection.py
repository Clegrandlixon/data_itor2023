from abc import ABC, abstractmethod
import copy
import random
import time

from itertools import product
from jmetal.core.operator import Injection
from jmetal.core.solution import RoutingSolution
from jmetal.problem.multiobjective.movrptw import MOVRPTW
from jmetal.problem.multiobjective.motsp import BOTSP

Addition = lambda x,y: x+y
Substraction = lambda x,y: x-y

"""
.. module:: injection
   :platform: Unix, Windows
   :synopsis: Module implementing injection operators.

.. moduleauthor:: Clément Legrand <clement.legrand4.etu@univ-lille.fr>
"""

class GenericPatternInjection(Injection[RoutingSolution], ABC):
    def __init__(self, problem, probability: float, diversificationFactor: int, allowReverse: bool):
        super(GenericPatternInjection, self).__init__(probability, diversificationFactor)

        self.allowReverse = allowReverse
        self.problem = problem
        # Return True if at least one pattern has been injected in the solution
        self.injected = False
        self.interestingData = {"PossibleInjections": [], "InitialObjectives": [], "Sizes": [],"Injected": [], "Alive":[], "Iterations":[]} # the index of the list corresponds to the number of iteration. Each element of Sizes/Alive is a dictionary

        ### Variables used during best_reconnect procedure ###
        self.R_bests = None 
        self.bestCost = None
        self.recursion = 0
        ###
        
        # Attribute that depends on the solution
        self.names_attributes = []
        self.weights_attributes = {}
        self.unfeasibility_attributes = []
        
    def reset_attributes(self):
        self.R_bests = None
        self.bestCost = None
        self.recursion = 0
        self.injected = False

    @abstractmethod
    def define_names_of_attributes_and_weights(self, solution):
        """ Return tuples (name, weight) of characteristics required for the evaluation of a fragment of the solution 
        """
        pass

    @abstractmethod
    def compute_information_fragment(self, fragment, solution, reverse = False):
        """ Compute the attributes of a fragment. It can depend on the problem solved
        """
        pass
    
    def update_2costs(self, value1, value2, operator):
        keys = self.names_attributes
        newValues = {i:0 for i in keys}
        for i in keys:
            newValues[i] = operator(value1[i], value2[i])
        return newValues

    def update_MultipleCosts(self, values, operator):
        newValues = {i:0 for i in self.names_attributes}
        for v in values:
            newValues = self.update_2costs(newValues, v, operator)
        return newValues    

    def cost_of_list_of_fragments(self, list_fragments):
        return self.update_MultipleCosts(list_fragments, Addition)


    def check_is_pattern_present(self, solution, pattern):
        l = len(pattern)
        list_routes = solution.structure
        start_pattern = pattern[0]
        is_present = False
        for r in list_routes:
            if start_pattern in r:
                i = r.index(start_pattern)
                if i+l-1 < len(r):
                    is_present = pattern == r[i:i+l]
                break
        return is_present

    def __compute_information_pattern(self, solution, pattern):
        attributes_pattern = solution.sequences[pattern[0]][pattern[0]]
        current_pattern = [pattern[0]]
        n = len(pattern)
        for i in range(1, n):
            next_customer = pattern[i]
            attributes_pattern = self.problem.concatenate_subsequences((current_pattern[0], current_pattern[-1]), attributes_pattern, (next_customer, next_customer), solution.sequences[next_customer][next_customer])
            current_pattern.append(next_customer)
        return attributes_pattern

    def cut_into_fragments(self, solution, pattern, removeDepot: bool):
        list_routes = solution.structure
        R_inv = [] # routes which not contain any customers in the pattern and thus are not modified
        R_init = [] # routes which contain at least one customer of pattern
        R_beg = [] # fragments of routes which start with the depot
        R_mid = [] # fragments of routes which don't contain the depot
        R_end = [] # fragments of routes which end with the depot

        for r in list_routes:
            frag = []
            inv = True
            for c in r:
                if c in pattern:
                    inv = False
                    if frag != []: # when routes contain two consecutive customers that belong to the pattern
                        if frag[0] == 0:
                            if len(frag) > 1 and removeDepot:
                                attributes_fragment = self.compute_information_fragment(frag[1:], solution, False)
                                R_beg.append((frag[1:], attributes_fragment))
                            elif not removeDepot:
                                attributes_fragment = self.compute_information_fragment(frag, solution, False)
                                R_beg.append((frag, attributes_fragment))
                        else:
                            attributes_fragment = self.compute_information_fragment(frag, solution, False)
                            if self.allowReverse:
                                reversed_fragment = self.compute_information_fragment(frag, solution, True)
                            else:
                                reversed_fragment = None
                            R_mid.append((frag, attributes_fragment, reversed_fragment)) # reversed fragments are used only when self.allowReverse is True 
                        frag = []
                else:
                    frag.append(c)
            if inv:
                attributes_fragment = self.compute_information_fragment(r, solution)
                R_inv.append((r,attributes_fragment))
            else:
                attributes_fragment = self.compute_information_fragment(r, solution)
                R_init.append((r,attributes_fragment))
                if frag != []:
                    if len(frag) > 1 and removeDepot:
                        attributes_fragment = self.compute_information_fragment(frag[:-1], solution)
                        R_end.append((frag[:-1], attributes_fragment))
                    elif not removeDepot:
                        attributes_fragment = self.compute_information_fragment(frag, solution)
                        R_end.append((frag, attributes_fragment))

        attributes_pattern = self.__compute_information_pattern(solution, pattern)
        if self.allowReverse:
            reversed_pattern = pattern.reverse()
            attributes_reversed_pattern = self.__compute_information_pattern(solution, reversed_pattern)
        else:
            attributes_reversed_pattern = None
        R_mid.append((pattern, attributes_pattern, attributes_reversed_pattern))
        self.R_bests = R_init.copy() # current best
        return R_inv, R_beg, R_mid, R_end

    def best_reconnect_PILS(self, solution: RoutingSolution, beg, mid, end, complete):
        """
        Apply the best_reconnect procedure from PILS
        reference: Florian Arnold et al. "PILS: Exploring high-order neighborhoods by pattern mining and injection" (2021)
        """
        (R_beg, cost_beg) = beg
        (R_mid, cost_mid) = mid
        (R_end, cost_end) = end
        (R_complete, cost_complete) = complete
        self.recursion += 1
        totalCost = self.update_MultipleCosts([cost_beg, cost_mid, cost_end, cost_complete], Addition)
        
        costSolution = sum([totalCost[i]*self.weights_attributes[i] for i in self.names_attributes])
        if self.recursion > 10000: # Keep this condition to avoid memory problems when the number of pieces to reconnect is too high -> TODO: new method to handle this issue: add the pattern in a new route
            return

        # maintain a set containing all the generated solutions during the execution. If the number is too high, then only keep non dominated ones
        if costSolution < self.bestCost: #and round(totalCost["TW"], 10) == 0 and totalCost["nQ"] == 0: # check that solutions are feasible
            if len(R_beg) == 0:
                self.R_bests = R_complete.copy()
                self.injected = True
                self.bestCost = costSolution
            else:
                f_beg = random.sample(R_beg, 1)[0]
                
                for f_mid in R_mid:
                    new_R_beg_normal = R_beg.copy()
                    new_R_beg_normal.remove(f_beg)
                    
                    new_R_beg_reverse = R_beg.copy()
                    new_R_beg_reverse.remove(f_beg)
                    
                    new_R_mid = R_mid.copy()
                    new_R_mid.remove(f_mid)

                    new_costMid = self.update_2costs(cost_mid, f_mid[1], Substraction) 
                    new_mid = (new_R_mid, new_costMid)

                    new_frag_normal = f_beg[0] + f_mid[0] # the new fragment (starts with depot)
                    attributes_frag_normal = self.problem.concatenate_subsequences((f_beg[0][0], f_beg[0][-1]), f_beg[1], (f_mid[0][0], f_mid[0][-1]), f_mid[1])
                    
                    new_R_beg_normal.append((new_frag_normal, attributes_frag_normal))
                    
                    new_costBeg_normal = self.update_2costs(self.update_2costs(cost_beg, f_beg[1], Substraction), new_R_beg_normal[-1][1], Addition)
                    new_beg_normal = (new_R_beg_normal, new_costBeg_normal)
                    
                    new_end = (R_end.copy(), cost_end)
                    new_complete = (R_complete.copy(), cost_complete)

                    self.best_reconnect_PILS(solution, new_beg_normal, new_mid, new_end, new_complete)
                    
                    if self.allowReverse:
                        f_mid[0].reverse()
                        new_frag_reverted = f_beg[0] + f_mid[0]
                        attributes_frag_reverted = self.problem.concatenate_subsequences((f_beg[0][0], f_beg[0][-1]), f_beg[1], (f_mid[0][0], f_mid[0][-1]), f_mid[2])

                        new_R_beg_reverse.append((new_frag_reverted, attributes_frag_reverted))    
                        
                        new_costBeg_reverse = self.update_2costs(self.update_2costs(cost_beg, f_beg[1], Substraction), new_R_beg_reverse[-1][1], Addition)
                        new_beg_reverse = (new_R_beg_reverse, new_costBeg_reverse)
                        self.best_reconnect_PILS(solution, new_beg_reverse, new_mid, new_end, new_complete)
                    
                if len(R_beg) != 1 or len(R_mid) == 0:
                    for f_end in R_end:
                        new_R_beg = R_beg.copy()
                        new_R_beg.remove(f_beg)
                        new_R_end = R_end.copy()
                        new_R_end.remove(f_end)

                        new_costEnd = self.update_2costs(cost_end, f_end[1], Substraction)
                        new_end = (new_R_end.copy(), new_costEnd)
                        new_costBeg = self.update_2costs(cost_beg, f_beg[1], Substraction)
                        new_beg = (new_R_beg.copy(), new_costBeg)


                        new_frag = f_beg[0] + f_end[0] # the new fragment (starts with depot)
                        attributes_frag = self.problem.concatenate_subsequences((f_beg[0][0], f_beg[0][-1]), f_beg[1], (f_end[0][0], f_end[0][-1]), f_end[1])

                        new_R = R_complete.copy()
                        new_R.append((new_frag, attributes_frag))

                        new_costR = self.update_2costs(cost_complete, new_R[-1][1], Addition)
                        new_complete = (new_R.copy(), new_costR)

                        new_mid = (R_mid.copy(), cost_mid)

                        self.best_reconnect_PILS(solution, new_beg, new_mid, new_end, new_complete)

    def create_solution(self, newRoutes, unchangedRoutes, solution: RoutingSolution):

        namesObjectives = self.problem.get_names_objectives()

        newSolution = RoutingSolution(solution.number_of_variables, solution.number_of_objectives)
        solution.sequences = None # free the sequences of solution
        newSolution.attributes = solution.attributes.copy()
        newSolution.variables = []
        newSolution.associatedProblem = solution.associatedProblem
        
        # define the structure and variables of newSolution
        allRoutes = newRoutes + unchangedRoutes
        for (i, attributes_i) in allRoutes:
            if i != [0,0]:
                for c in i:
                    if c != 0:
                        newSolution.variables.append(c-1)
                
                for k in range(newSolution.number_of_objectives):
                    newSolution.objectives[k] += attributes_i[namesObjectives[k]]
                    
                newSolution.structure.append(i.copy())

        self.problem.compute_subsequences(self.problem.get_tour(newSolution), newSolution, False)
        newSolution.objectives = list(map(lambda x: round(x,2), newSolution.objectives))
        return newSolution

    def inject_one_pattern(self, solution: RoutingSolution, pattern):
        """
        Try to inject the pattern into the solution by using the injection of PILS method.
        Weights are used to compute the fitness of the solution
        """

        # first cut the routes of the solution into fragments
        R_inv, R_beg, R_mid, R_end = self.cut_into_fragments(solution, pattern, removeDepot=False)
        random.shuffle(R_mid) # bring diversity during the reconnection if all possibilities can not be tested due to recursion stack issue

        attributesINV = self.cost_of_list_of_fragments([i[1] for i in R_inv])
        costINV = sum([attributesINV[i]*self.weights_attributes[i] for i in self.names_attributes])
        self.bestCost = solution.attributes["weights"][0] * solution.objectives[0] + solution.attributes["weights"][1] * solution.objectives[1] - costINV

        cost_beg = self.cost_of_list_of_fragments([i[1] for i in R_beg])
        cost_mid = self.cost_of_list_of_fragments([i[1] for i in R_mid])
        cost_end = self.cost_of_list_of_fragments([i[1] for i in R_end])
        
        self.best_reconnect_PILS(solution, (R_beg, cost_beg), (R_mid, cost_mid), (R_end, cost_end), ([], {i:0 for i in self.names_attributes}))
        newRoutes = self.R_bests # R_bests contains only the modified routes
   
        if self.injected:
            return self.create_solution(newRoutes, R_inv, solution)
        else:
            return solution
        

    def execute(self, solution: RoutingSolution, chosenPatterns: list) -> RoutingSolution:
        """ Tentatively inject patterns from chosenPatterns one by one.  
        A pattern is kept only in case of improvement.

        :param solution: The solution that undergoes the injection
        :param chosenPatterns: The list of patterns that are tentatively injected
        :return: A tuple (new solution, applied) containing the new solution and a boolean which is True when the injection has been applied 
        """
        
        nextSolution = solution
        self.atLeastOneinjected = False

        if random.random() > self.probability:
            return nextSolution, False

        self.define_names_of_attributes_and_weights(solution)
        current_iter = 0
        for pattern in chosenPatterns:
            current_iter += 1
            # verify that the pattern is not already present in the solution
            if not self.check_is_pattern_present(nextSolution, pattern):

                nextSolution = self.inject_one_pattern(nextSolution, pattern)
                
                self.reset_attributes()

        return nextSolution, True

    def get_name(self):
        return 'Multi-Objective pattern injection'

class PatternInjectionMOTSP(GenericPatternInjection):
    def __init__(self, problem: BOTSP, probability, diversificationFactor):
        super(PatternInjectionMOTSP, self).__init__(problem, probability, diversificationFactor, allowReverse = True)

    def define_names_of_attributes_and_weights(self, solution: RoutingSolution):
        self.names_attributes = ['cost1', 'cost2']
        self.weights_attributes = {'cost1': solution.attributes["weights"][0], 'cost2':solution.attributes["weights"][1]}
        self.unfeasibility_attributes = []
        
    def compute_information_fragment(self, fragment, solution, reverse: bool = True):
        """
        Compute the attributes of a fragment of solution (cost1 and cost2)
        The solution must have its sequences up to date

        :param fragment: The fragment that is evaluated (the depot is added)
        :param solution: The solution that contains the fragment
        :param reverse: Specify whether the fragment is reversed or not
        :return: A list containing the attributes of the fragment
        """
        if len(fragment) == 1:
            attributes_route = solution.sequences[fragment[0]][fragment[0]]
        elif fragment[0] == 0 and fragment[-1] == 0:
            attributes_route = solution.sequences[fragment[1]][fragment[-2]]
            attributes_route = self.problem.add_depot_to_sequence((fragment[1], fragment[-2]), attributes_route, solution)
        elif fragment[0] == 0:
            attributes_route = solution.sequences[fragment[1]][fragment[-1]]
            attributes_route = self.problem.add_depot_to_left((fragment[1], fragment[-1]), attributes_route, solution)
        elif fragment[-1] == 0:
            attributes_route = solution.sequences[fragment[0]][fragment[-2]]
            attributes_route = self.problem.add_depot_to_right((fragment[0], fragment[-2]), attributes_route, solution)
        else:
            if reverse:
                attributes_route = solution.reverted_sequences[fragment[0]][fragment[-1]]
            else:
                attributes_route = solution.sequences[fragment[0]][fragment[-1]]
        return attributes_route    

    def get_name(self):
        return 'Multi-Objective pattern injection for BOTSP'


class PatternInjectionMOVRPTW(GenericPatternInjection):
    def __init__(self, problem: MOVRPTW, probability, diversificationFactor):
        super(PatternInjectionMOVRPTW, self).__init__(problem, probability, diversificationFactor, allowReverse= False)

    def define_names_of_attributes_and_weights(self, solution: RoutingSolution):
        """
        Return the names of the characteristics necessary for the evaluation of a fragment of the solution 
        associated with their weights
        """
        self.names_attributes = ['nQ', 'C', 'WT', 'TW']
        self.weights_attributes = {'nQ': 5000, 'C': solution.attributes["weights"][0], 'WT': solution.attributes["weights"][1], 'TW': 50000}
        self.unfeasibility_attributes = ['nQ', 'TW']
    
    def compute_information_fragment(self, fragment, solution: RoutingSolution, reverse = False):
        """
        Compute the attributes of a fragment of solution (duration, cost, waiting time...)
        The solution must have its sequences up to date

        :param fragment: The fragment that is evaluated (the depot is added)
        :param solution: The solution that contains the fragment
        :param reverse: Specify whether the fragment is reversed or not. It is set to False in the case of the movrptw
        :return: A list containing the attributes of the fragment
        """
        if len(fragment) == 1:
            attributes_route = solution.sequences[fragment[0]][fragment[0]]
        elif fragment[0] == 0 and fragment[-1] == 0:
            attributes_route = solution.sequences[fragment[1]][fragment[-2]]
            attributes_route = self.problem.add_depot_to_sequence((fragment[1], fragment[-2]), attributes_route, solution)
        elif fragment[0] == 0:
            attributes_route = solution.sequences[fragment[1]][fragment[-1]]
            attributes_route = self.problem.add_depot_to_left((fragment[1], fragment[-1]), attributes_route, solution)
        elif fragment[-1] == 0:
            attributes_route = solution.sequences[fragment[0]][fragment[-2]]
            attributes_route = self.problem.add_depot_to_right((fragment[0], fragment[-2]), attributes_route, solution)
        else:
            attributes_route = solution.sequences[fragment[0]][fragment[-1]]
        
        return attributes_route    

    def get_name(self):
        return 'Multi-Objective pattern injection for BOVRPTW'