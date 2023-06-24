import logging
import os
from pathlib import Path
from typing import List

from jmetal.core.solution import FloatSolution, Solution, RoutingSolution
from jmetal.util.archive import NonDominatedSolutionsArchive, Archive

LOGGER = logging.getLogger('jmetal')


"""
.. module:: solutions
   :platform: Unix, Windows
   :synopsis: Utils to print solutions.

.. moduleauthor:: Antonio J. Nebro <ajnebro@uma.es>, Antonio Benítez-Hidalgo <antonio.b@uma.es>
"""


def get_non_dominated_solutions(solutions: List[Solution]) -> List[Solution]:
    archive: Archive = NonDominatedSolutionsArchive()

    for solution in solutions:
        archive.add(solution)

    return archive.solution_list


def read_solutions(filename: str) -> List[FloatSolution]:
    """ Reads a reference front from a file.

    :param filename: File path where the front is located.
    """
    front = []

    if Path(filename).is_file():
        with open(filename) as file:
            for line in file:
                vector = [float(x) for x in line.split()]

                solution = FloatSolution([], [], len(vector))
                solution.objectives = vector

                front.append(solution)
    else:
        LOGGER.warning('Reference front file was not found at {}'.format(filename))

    return front


def print_variables_to_file(solutions, filename: str):
    #LOGGER.info('Output file (variables): ' + filename)

    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    except FileNotFoundError:
        pass

    if type(solutions) is not list:
        solutions = [solutions]

    with open(filename, 'w') as of:
        for solution in solutions:
            for variables in solution.variables:
                of.write(str(variables) + " ")
            if "weights" in solution.attributes.keys():
                of.write(str(solution.attributes["weights"])) # add the weights to have access to the number of vehicles when evaluating a solution
            of.write("\n")
    
def print_variables_to_screen(solutions):
    if type(solutions) is not list:
        solutions = [solutions]

    for solution in solutions:
        print(solution.variables[0])


def print_function_values_to_file(solutions, filename: str):
    #LOGGER.info('Output file (function values): ' + filename)
    
    front_names = ''

    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    except FileNotFoundError:
        pass

    if type(solutions) is not list:
        solutions = [solutions]

    with open(filename, 'w') as of: # specific format to read the fronts
        #cpt = 1
        for solution in solutions:
            #of.write(str(cpt) + '\t')
            #cpt += 1
            for function_value in solution.objectives:
                of.write(str(function_value) + '\t')
            of.write('\n')


def print_function_values_to_screen(solutions):
    if type(solutions) is not list:
        solutions = [solutions]

    for solution in solutions:
        print(str(solutions.index(solution)) + ": ", sep='  ', end='', flush=True)
        print(solution.objectives, sep='  ', end='', flush=True)
        print()

def print_structures_to_file(solutions, filename: str):
    #LOGGER.info('Output file (variables): ' + filename)

    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    except FileNotFoundError:
        pass

    if type(solutions) is not list:
        solutions = [solutions]

    with open(filename, 'w') as of:
        for solution in solutions:
            line = ""
            for route in solution.structure:
                for c in route:
                    line += str(c) + " "
                line += "# "
            line += "| "
            if "weights" in solution.attributes.keys():
                # add the weights to have access to the number of vehicles when evaluating a solution
                for w in solution.attributes["weights"]:
                    line += str(w) + " "
            line += "\n"
            of.write(line)