import os
from scipy import stats
from jmetal.core.solution import RoutingSolution
from jmetal.util.archive import NonDominatedSolutionsArchive
from jmetal.problem.multiobjective.movrptw import MOVRPTW
import matplotlib.pyplot as plt
# use the files allFUN.tsv

def read_file_toList(file):
    # index i is the i-th line of the file
    values = []
    with open(file, 'r') as of:
        lines = of.readlines()
        data = [line.lstrip() for line in lines if line != ""]
        for line in data:
            lineValues = [float(i) for i in line.split()]
            values.append(lineValues)
    return values

def read_variables(file):
    listVariables = []
    with open(file, 'r') as of:
        lines = of.readlines()
        data = [line.lstrip() for line in lines if line !=""]
        for line in data:
            rawVariables = line
            variables = [int(i) for i in rawVariables.split()]
            listVariables.append((variables, None))
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

def write_list_toFile(listValues, outputPath):
    with open(outputPath, 'w') as of:
        for i in listValues:
            line = ""
            for j in i:
                line += str(j) + "\t"
            line += "\n"
            of.write(line)
    return 

def print_structures_to_file(solutions, filename: str):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    except FileNotFoundError:
        pass

    with open(filename, 'w') as of:
        for solution in solutions:
            line = ""
            for route in solution.structure:
                for c in route:
                    line += str(c) + " "
                line += "# "
            line += "| "
            if "weights" in solution.attributes.keys():
                for w in solution.attributes["weights"]:
                    line += str(w) + " "
            line += "\n"
            of.write(line)

def print_function_values_to_file(solutions, filename: str):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    except FileNotFoundError:
        pass

    with open(filename, 'w') as of: # specific format to read the fronts
        for solution in solutions:
            for function_value in solution.objectives:
                of.write(str(function_value) + '\t')
            of.write('\n')

def merge_objectiveSpaces(space1, space2):
    newObjectiveSpace= set()
    for obj in space1 + space2:
        t = obj[0], obj[1]
        newObjectiveSpace.add(t)
    return list(newObjectiveSpace)

def create_objectiveSpace(allFiles):
    for (input, outputPath, outputFile, instance) in allFiles:
        print(instance)
        completeOutputPath = os.path.join(outputPath, outputFile)
        
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)

        # if outputfile exists, then update it    
        if os.path.exists(completeOutputPath):
            currentObjectiveSpace = read_file_toList(completeOutputPath)
        else:
            currentObjectiveSpace = []

        newObjectiveSpace = read_file_toList(input)
        
        finalObjectiveSpace = merge_objectiveSpaces(currentObjectiveSpace, newObjectiveSpace)

        write_list_toFile(finalObjectiveSpace, completeOutputPath)

        # create the plot of the front
        x, y = [], []
        for s in finalObjectiveSpace:
            x.append(s[0])
            y.append(s[1])

        MEDIUM_SIZE = 13
        BIGGER_SIZE = 15
        plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
        plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
        plt.rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
        plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize
        plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
        plt.figure(figsize=[8, 8])
        plt.scatter(x,y)
        plt.title('Objective Space of ' + instance["name"]+instance["id"] + '-' + instance["size"])
        plt.xlabel('Total traveled distance')
        plt.ylabel('Total waiting time')
        output_figure = os.path.join(outputPath, 'space.png')
        plt.savefig(output_figure)
        plt.close()

    return

def corelation(objectives):
    X = [i[0] for i in objectives]
    Y = [i[1] for i in objectives]
    slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
    return round(r_value, 2)


def compute_corelations(allFiles):
    for (input, outputPath, outputFile) in allFiles:
        completeOutputPath = os.path.join(outputPath, outputFile)
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)
        
        objectiveSpace= read_file_toList(input)
        c = corelation(objectiveSpace)

        write_list_toFile([[c]], completeOutputPath)

def update_reference_front(benchmark, instance, inputPath):
    # create the FUN file and the STR file, VAR file is useless since it can be obtained with the STR file
    # create also the figure of the front
    archive = NonDominatedSolutionsArchive()

    outputPath = os.path.join("resources", "reference_front", "VRPTW", benchmark, benchmark+"_"+instance["size"], instance["name"]+instance["id"])

    outputFun = os.path.join(outputPath, "FUN.tsv")
    outputStr = os.path.join(outputPath, "STR.tsv")

    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    
    existingFun = []
    existingStr = []
    
    if os.path.exists(outputFun) and os.path.exists(outputStr):
        existingFun = read_file_toList(outputFun)
        existingStr = read_structures(outputStr)

        for i in range(len(existingFun)):
            solution = RoutingSolution(int(instance["size"]), 2)
            solution.objectives = existingFun[i]
            solution.structure = existingStr[i][0]
            solution.attributes["weights"] = existingStr[i][1] if not existingStr[i][1] is None else []
            archive.add(solution)

    inputFun = os.path.join(inputPath, "ndFUN.tsv")
    inputStr = os.path.join(inputPath, "ndSTR.tsv")

    newFun = read_file_toList(inputFun)
    newStr = read_structures(inputStr)

    for j in range(len(newFun)):
        solution = RoutingSolution(int(instance["size"]), 2)
        solution.objectives = newFun[j]
        solution.structure = newStr[j][0]
        solution.attributes["weights"] = newStr[j][1] if not newStr[j][1] is None else []
        archive.add(solution)

    print_function_values_to_file(archive.solution_list, outputFun)
    print_structures_to_file(archive.solution_list, outputStr)

    # create the plot of the front
    x, y = [], []
    for s in archive.solution_list:
        x.append(s.objectives[0])
        y.append(s.objectives[1])

    MEDIUM_SIZE = 13
    BIGGER_SIZE = 15
    plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=BIGGER_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=MEDIUM_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=MEDIUM_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
    plt.figure(figsize=[8, 8])
    plt.scatter(x,y)
    plt.title('Pareto-front of ' + instance["name"]+instance["id"] + '-' + instance["size"])
    plt.xlabel('Total traveled distance')
    plt.ylabel('Total waiting time')
    output_figure = os.path.join(outputPath, 'front.svg')
    plt.savefig(output_figure)
    plt.close()
    return



DATAFOLDER = "performance_results"
ALGORITHMS = ["fbd1", "fbd2", "fbd3", "moeadls"]
BENCHMARK = "Homberger"
NBRUNS = 30

generated_instances = []
if BENCHMARK == "Generated":
    for l1 in range(1, 4):
        for l2 in ['L', 'S']:
            for l3 in ['T', 'W']:
                for l4 in ['R']:
                    instance = {}
                    instance['size'] = '100'
                    instance['name'] = l4 + l2 + l3
                    instance['id'] = str(l1)
                    generated_instances.append(instance)

elif BENCHMARK == "Solomon":
    numbers_instances_C = ['101', '102', '103', '104', '105', '106', '107', '108', '109', '201', '202', '203', '204', '205', '206', '207', '208']
    numbers_instances_R = ['101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '201', '202', '203', '204', '205', '206', '207', '208', '209', '210', '211']
    numbers_instances_RC = ['101', '102', '103', '104', '105', '106', '107', '108', '201', '202', '203', '204', '205', '206', '207', '208']
    number_instances = {}
    number_instances['C'] = numbers_instances_C
    number_instances['R'] = numbers_instances_R
    number_instances['RC'] = numbers_instances_RC

    for size in ['100']:
        for type in ['C', 'R']:
            for id in number_instances[type]:
                instance = {}
                instance['size'] = size
                instance['name'] = type
                instance['id'] = id
                generated_instances.append(instance)

elif BENCHMARK == "Homberger":
    idInstance = [str(i) for i in range(1,11)]
    typeInstances_Hom = ["C1_2_", "C2_2_", "R1_2_", "R2_2_"] #["C1_2_", "C2_2_", "R1_2_", "R2_2_"]

    for size in ['200']:
        for type in typeInstances_Hom:
            for id in idInstance:
                instance = {}
                instance['size'] = size
                instance["name"] = type
                instance["id"] = id
                generated_instances.append(instance)



"""
allFiles = []
for algo in ALGORITHMS:
    for idRun in range(1,NBRUNS+1):
        for instance in generated_instances:
            inputPath = os.path.join(DATAFOLDER, algo, BENCHMARK, BENCHMARK+"_"+instance["size"], instance["name"] + instance["id"], "Run" + str(idRun), "Final", "allFUN.tsv")
            outputPath = os.path.join("objectiveSpace", BENCHMARK, BENCHMARK+"_"+instance["size"], instance["name"] + instance["id"])
            outputFile = "space.tsv" 
            allFiles.append((inputPath, outputPath, outputFile, instance))

create_objectiveSpace(allFiles)
"""

"""
allFiles = []
for instance in generated_instances:
    #inputPath = os.path.join("objectiveSpace", BENCHMARK, BENCHMARK+"_"+instance["size"], instance["name"] + instance["id"], "space.tsv")
    inputPath = os.path.join("resources", "reference_front", "VRPTW", BENCHMARK, BENCHMARK+"_"+instance["size"], instance["name"] + instance["id"], "FUN.tsv")
    #outputPath = os.path.join("objectiveSpace", BENCHMARK, BENCHMARK+"_"+instance["size"], instance["name"] + instance["id"])
    outputPath = os.path.join("resources", "reference_front", "VRPTW", BENCHMARK, BENCHMARK+"_"+instance["size"], instance["name"] + instance["id"])
    outputFile = "correlation.tsv" 
    allFiles.append((inputPath, outputPath, outputFile))

compute_corelations(allFiles)
"""


for algo in ALGORITHMS:
    for idRun in range(1,NBRUNS+1):
        for instance in generated_instances:
            print(algo, idRun, instance)
            inputPath = os.path.join(DATAFOLDER, algo, BENCHMARK, BENCHMARK+"_"+instance["size"], instance["name"] + instance["id"], "Run" + str(idRun), "Final")
            update_reference_front(BENCHMARK, instance, inputPath)

