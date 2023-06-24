import os
import numpy
from jmetal.core.solution import PermutationSolution, RoutingSolution


# format Objectives: SNAPSHOT.FUN.k.tsv
# format Solutions: SNAPSHOT.VAR.k.tsv

def read_objectives(file):
    listObjectives = []
    with open(file, 'r') as of:
        lines = of.readlines()
        data = [line.lstrip() for line in lines if line !=""]
        for line in data:
            objectives = [float(i) for i in line.split()[:]]
            listObjectives.append(objectives)
    return listObjectives

def read_variables(file):
    listVariables = []
    with open(file, 'r') as of:
        lines = of.readlines()
        data = [line.lstrip() for line in lines if line !=""]
        for line in data:
            #rawVariables, rawWeights = line.split('[')
            rawVariables = line
            variables = [int(i) for i in rawVariables.split()]
            #weights = [float(i) for i in rawWeights[:-2].split()]
            listVariables.append((variables, None))#, weights))
    return listVariables

def read_structures(file):
    listVariables = []
    with open(file, 'r') as of:
        lines = of.readlines()
        data = [line.lstrip() for line in lines if line !=""]
        for line in data:
            rawRoutes, rawWeights = line.split('|')
            listRoutes = []
            for rawRoute in rawRoutes.split('# '):
                route = []
                for i in rawRoute.split(' ')[:-1]:
                    route.append(int(i))
                if route != []:
                    listRoutes.append(route)

            if len(rawWeights) > 2:
                weights = [float(i) for i in rawWeights[:-1].split()]
            else:
                weights = None
            listVariables.append((listRoutes, weights))
    return listVariables

def read_checkpoint_k(path, k, problem): # TODO modify since the weights are recorded with the solution
    fileObjectives = os.path.join(path, 'SNAPSHOT.FUN.'+str(k)+'.tsv')
    listObjectives = read_objectives(fileObjectives)

    fileVariables = os.path.join(path, 'SNAPSHOT.VAR.'+str(k)+'.tsv')
    listVariables = read_variables(fileVariables)

    n = len(listObjectives)
    listSolutions = []

    for i in range(n):
        solution = PermutationSolution(problem.number_of_variables, problem.number_of_objectives)
        solution.objectives = listObjectives[i]
        solution.variables = listVariables[i]
        solution.weights = [0.8, 0.2]
        problem.evaluate(solution)
        tour = [0] + [i+1 for i in solution.variables]
        problem.compute_subsequences(tour, solution, reverse = False)
        listSolutions.append(solution)
    return listSolutions

def generate_setSolutions(listIndices, path, problem):
    setSolutions = []
    for k in listIndices:
        solutions = read_checkpoint_k(path, k, problem)
        setSolutions += solutions
    #return random.sample(setSolutions, 10)
    return setSolutions

def read_final_results_oldFormat(path, objFile, varFile, problem, normalizeObjectives = False):
    """
    TODO: bTSP
    Read the front of a VRPTW instance. 
    """
    fileObjectives = os.path.join(path, objFile)
    listObjectives = read_objectives(fileObjectives)
    n = len(listObjectives)
    k = len(listObjectives[0])
    
    if normalizeObjectives:
        maxObjs = []
        minObjs = []
        
        for i in range(k):
            objI = [l[i] for l in listObjectives]
            maxObjs.append(max(objI))
            minObjs.append(min(objI))
        print(maxObjs, minObjs)
        for i in range(n):
            listObjectives[i] = [(listObjectives[i][j]-minObjs[j])/(maxObjs[j]-minObjs[j]) for j in range(k)]

    fileVariables = os.path.join(path, varFile)
    listVariables = read_variables(fileVariables)
    
    listSolutions = []
    cpt_false = 0
    for i in range(n):
        solution = RoutingSolution(len(listVariables[0][0]), k) #len(listVariables[0][1]))
        solution.variables = listVariables[i][0]
        """
        solution.attributes["weights"] = listVariables[i][1]
        problem.evaluate(solution)
        solution.objectives = listObjectives[i] # normalize objectives
        listSolutions.append(solution)
        """
        weights = [(i/10, 1-i/10) for i in range(20)]
        found = False
        for w in weights:
            solution.attributes["weights"] = w
            problem.evaluate(solution)
            if solution.objectives == listObjectives[i]:
                found = True
                break
        if found:
            listSolutions.append(solution)
        else:
            cpt_false += 1
            solution.structure = [[0] + [i+1 for i in solution.variables] + [0]] # not represantative but contains all the patterns
            listSolutions.append(solution)
        
    print("Number of structures not found: ", cpt_false)
    return listSolutions

def read_final_results(path, objFile, varFile, normalizeObjectives = False):
    """
    TODO: bTSP
    Read the front of a VRPTW instance. 
    """
    fileObjectives = os.path.join(path, objFile)
    listObjectives = read_objectives(fileObjectives)
    n = len(listObjectives)
    k = len(listObjectives[0])
    
    if normalizeObjectives:

        maxObjs = []
        minObjs = []
        
        for i in range(k):
            objI = [l[i] for l in listObjectives]
            maxObjs.append(max(objI))
            minObjs.append(min(objI))
        print(maxObjs, minObjs)

        for i in range(n):
            listObjectives[i] = [(listObjectives[i][j]-minObjs[j])/(maxObjs[j]-minObjs[j]) for j in range(k)]
    
    fileVariables = os.path.join(path, varFile)
    listStructures = read_structures(fileVariables)
    
    listSolutions = []

    for i in range(n):
        routes = listStructures[i][0]
        variables = []
        for r in routes:
            for j in r:
                if j > 0:
                    variables.append(j-1)

        solution = RoutingSolution(len(variables), k) #len(listVariables[0][1]))

        solution.variables = variables
        solution.structure = listStructures[i][0]
        if listStructures[i][1] != None:
            solution.attributes["weights"] = listStructures[i][1]
        solution.objectives = listObjectives[i]
        listSolutions.append(solution)
    return listSolutions