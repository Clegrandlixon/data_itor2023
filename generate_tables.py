import os
import numpy as np

def read_file_toList(file, startingLine = 0):
    # index i is the i-th line of the file
    values = []
    with open(file, 'r') as of:
        lines = of.readlines()
        data = [line.lstrip() for line in lines if line != ""]
        for line in data[startingLine:]:
            lineValues = [float(i) for i in line.split()]
            values.append(lineValues)
    return values

def write_list_toFile(listValues, outputPath):
    with open(outputPath, 'w') as of:
        for i in listValues:
            line = ""
            for j in i:
                line += str(j) + "\t"
            line += "\n"
            of.write(line)
    return 

def find_extrema(file):
    values = read_file_toList(file)
    nbObjectives = len(values[0])
    ideal = []
    nadir = []
    for j in range(nbObjectives):
        ideal.append(min([i[j] for i in values]))
        nadir.append(max([i[j] for i in values]))
    return ideal, nadir

def obtain_ideal_nadir_size(benchmark, instances):
    ideal, nadir, size = [], [], []
    for instance in instances:
        path = os.path.join("resources", "reference_front", "VRPTW", benchmark, benchmark+"_"+instance["size"], instance["name"]+instance["id"], "FUN.tsv")
        ideal_Instance, nadir_Instance = find_extrema(path)
        size_Instance = read_file_toList(path)
        ideal.append(ideal_Instance)
        nadir.append(nadir_Instance)
        size.append(len(size_Instance))
    return ideal, nadir, size

def obtain_correlations(benchmark, instances):
    correlations = []
    for instance in instances:
        path = os.path.join("resources", "reference_front","VRPTW", benchmark, benchmark+"_"+instance["size"], instance["name"]+instance["id"], "correlation.tsv")
        value = read_file_toList(path)
        correlations.append(value[0][0])
    return correlations

def obtain_instances(instances):
    nameInstances = []
    for instance in instances:
        nameInstances.append(instance["name"] + instance["id"])
    return nameInstances

def create_table_instances(benchmark, instances, outputPath, outputFile):

    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    completePath = os.path.join(outputPath, outputFile)

    header = "Instance & Correlation & Front Size & Best Ideal & Best Nadir \\\\\n"
    nbLines = len(instances)

    nameInstances = obtain_instances(instances)
    correlations = obtain_correlations(benchmark, instances)
    ideal, nadir, size = obtain_ideal_nadir_size(benchmark, instances)

    results = [nameInstances, correlations, size, ideal, nadir]
    with open(completePath, 'w') as of:
        of.write(header)
        for i in range(nbLines):
            line = ""
            for j in range(len(results)):
                line += str(results[j][i]) + " & "
            line += "\\\\\n"
            of.write(line)
    return

def obtain_ttr(metrics, threshold):
    for l in metrics:
        if l[4] > threshold:
            return l[1]
    return metrics[-1][1]

def create_line_algorithm(instance, runs, threshold, startingPath):
    sizes = []
    uhv = []
    ttr = []
    for i in range(runs[0], runs[1]+1):
        inputPath = os.path.join(startingPath, instance["name"]+instance["id"], "Run"+str(i), "Final", "METRICS.tsv" )
        metrics = read_file_toList(inputPath, 1)
        sizes.append(metrics[-1][2])
        uhv.append(metrics[-1][4])
        ttr.append(obtain_ttr(metrics, threshold))
    line = instance["name"] + instance["id"] + " & " + str(round(np.mean(sizes), 1)) + " & " + str(round(np.mean(uhv), 4)) + " & " + str(round(np.mean(ttr), 1)) + "\\\\\n"
    return line

def create_table_algorithm(benchmark, algorithm, instances, runs, threshold, outputPath):
    header = "Instance & Avg Front Size & Avg uHV & TTR ("+str(threshold*100)+"\%) \\\\\n"
    
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    
    outputFile = os.path.join(outputPath, "table_"+benchmark+'_'+algorithm+".tsv")

    with open(outputFile, 'w') as of:
        of.write(header)
    
    for instance in instances:
        startingPath = os.path.join("performance_results", algorithm, benchmark, benchmark+"_"+instance["size"])
        line = create_line_algorithm(instance, runs, threshold, startingPath)

        with open(outputFile, "a+") as of:
            of.write(line)
    return

def create_specific_table(benchmark, algorithms, instances, runs, threshold, outputPath):
    header = "Instance & "
    header_alg = "Size & uHV & Time ("+str(threshold*100)+"\%)"

    outputFile = os.path.join(outputPath, "table_"+benchmark+'_'+"spec.tsv")

    for instance in instances:
        line = ""
        for algorithm in algorithms:
            startingPath = os.path.join("performance_results", algorithm, benchmark, benchmark+"_"+instance["size"])
            part_line = create_line_algorithm(instance, runs, threshold, startingPath)
            line += part_line
    
        with open(outputFile, "a+") as of:
            of.write(line)
    return 

def create_line_dataFrame(instance, algorithm, run, threshold, inputPath):
    metrics = read_file_toList(inputPath, 1)
    uhv = metrics[-1][4]
    ttr = obtain_ttr(metrics, threshold)
    line = instance["name"] + "\t" + instance["id"] + "\t" + algorithm + "\t" + str(run) + "\t" + str(uhv) + "\t" + str(ttr) + "\n"
    return line

def create_dataFrame_R(benchmark, instances, algorithms, nbRuns, threshold, outputPath):
    header = "Category \t ID \t Algorithm \t idRun \t HV \t Time\n"

    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    
    outputFile = os.path.join(outputPath, "dataFrame_"+benchmark+".tsv")

    with open(outputFile, 'w') as of:
        of.write(header)

    for instance in instances:
        for algorithm in algorithms:
            for run in range(1,nbRuns+1):
                inputPath = os.path.join("performance_results", algorithm, benchmark, benchmark+"_"+instance["size"], instance["name"]+instance["id"], "Run"+str(run), "Final", "METRICS.tsv")
                line = create_line_dataFrame(instance, algorithm, run, threshold, inputPath)
                with open(outputFile, "a+") as of:
                    of.write(line)
    return 

def decimals(precision, max):
    l = []
    for i in range(1, max+1):
        d = str(i)
        l.append('0'*(precision-len(d))+d)
    return l

DATAFOLDER = "results_cluster"
ALGORITHMS = ["moeadls", "fbd1", "fbd2", "fbd3", "bd1", "bd2", "bd3"]
BENCHMARK = "Solomon"
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
    number_instances = {}
    number_instances['C1'] = decimals(2, 9)
    number_instances['C2'] = decimals(2, 8)
    number_instances['R1'] = decimals(2, 12)
    number_instances['R2'] = decimals(2, 11)
    number_instances['RC1'] = decimals(2, 8)
    number_instances['RC2'] = decimals(2, 8)

    for size in ['100']:
        for type in ['C1', 'C2', 'R1', 'R2']:
            for id in number_instances[type]:
                instance = {}
                instance['size'] = size
                instance['name'] = type
                instance['id'] = id
                generated_instances.append(instance)

elif BENCHMARK == "Homberger":
    idInstance = ["_2_"+str(i) for i in range(1,11)]
    typeInstances_Hom = ["C1", "C2", "R1", "R2"]

    for size in ['200']:
        for type in typeInstances_Hom:
            for id in idInstance:
                instance = {}
                instance['size'] = size
                instance["name"] = type
                instance["id"] = id
                generated_instances.append(instance)

"""
outputPath = os.path.join("Results", BENCHMARK, BENCHMARK+"_"+instance["size"])
outputFile = "table.tsv"
create_table_instances(BENCHMARK, generated_instances, outputPath, outputFile)
"""
"""
outputPath = os.path.join("Results", BENCHMARK, BENCHMARK+"_"+instance["size"])
for algorithm in ALGORITHMS:
    create_table_algorithm(BENCHMARK, algorithm, generated_instances, [1,25], 0.80, outputPath)
"""

outputPath = os.path.join("Results", BENCHMARK, BENCHMARK+"_"+instance["size"])
create_dataFrame_R(BENCHMARK, generated_instances, ALGORITHMS, 25, 0.80, outputPath)

