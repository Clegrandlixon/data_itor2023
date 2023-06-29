import os
import subprocess
from multiprocessing import Pool

## Parameters
populationSize = [20,40,60,80,100]
granularity = [10,25,50,75,100]
probabilityCrossover = [0.00, 0.10, 0.25, 0.50, 0.75, 1.00]
probabilityLocalSearch = [0.00, 0.10, 0.25, 0.50, 0.75, 1.00]
nbGroups = [1,10,25,50,75,100]
maximumSizePattern = [2,5,8]
numberPatternInjected = [25,50,75,100]
probabilityInjection = [0.00, 0.10, 0.25, 0.50, 0.75, 1.00]
exploration = ["BEST", "FIRST-BEST"]
metric = ["d1", "d2", "d3"]

#allParameters = {"populationSize": populationSize, "granularity": granularity, "probabilityCrossover": probabilityCrossover, "probabilityLocalSearch": probabilityLocalSearch, "maximumSizePattern": maximumSizePattern, "nbGroups":nbGroups, "numberPatternInjected":numberPatternInjected, "probabilityInjection":probabilityInjection}
allParameters = [populationSize, granularity, probabilityCrossover, probabilityLocalSearch, nbGroups, maximumSizePattern, numberPatternInjected, probabilityInjection, exploration, metric]
namesParameters = ["populationSize", "granularity", "probabilityCrossover", "probabilityLocalSearch", "nbGroups", "maximumSizePattern", "numberPatternInjected", "probabilityInjection", "lsStrategy", "metric"]

## Instances 
# Generated
id_instances = ['1', '2', '3', '4', '5']
type_instances = []
l1 = ['R']
l2 = ['S', 'L'] 
l3 = ['T', 'W'] 
for a in l1:
    for b in l2:
        for c in l3:
            type_instances.append(a+b+c)

##  Configurations provided
# Order: popSize, granularity, crossover, ls, nb of groups, max size of pattern, nb of patterns injected, injection 
# Random configurations
rd1 = [40, 50, 0.25, 0.75, 5, 7, 60, 0.50]
rd2 = [60, 100, 0.10, 0.00, 10, 3, 20, 0.50]
rd3 = [20, 50, 0.10, 0.10, 20, 5, 20, 0.50]
rd4 = [80, 100, 1.00, 0.50, 5, 7, 60, 0.75]
rd5 = [100, 100, 0.10, 0.25, 1, 5, 20, 0.25]
#rd6 = [80, 10, 0.90, 0.90, 80, 5, 60, 0.00]
#rd7 = [60, 10, 0.25, 1.00, 1, 5, 100, 1.00]
#rd8 = [40, 75, 0.25, 0.90, 40, 7, 100, 0.75]
#rd9 = [100, 75, 0.90, 0.50, 1, 3, 20, 0.50]
#rd10 = [40, 10, 0.75, 0.75, 3, 7, 20, 0.90]

# Elite Configurations
# Elite for Clustered instances
#el1 = [20, 50, 0.50, 0.10, 25, 5, 50, 1.00, "FIRST-BEST", "d1"]
#el2 = [40, 75, 0.25, 0.10, 10, 8, 50, 1.00, "FIRST-BEST", "d2"]
#el3 = [40, 50, 0.25, 0.10, 25, 5, 75, 1.00, "FIRST-BEST", "d3"]
#el4 = [20, 75, 0.50, 0.10, 100, 5, 50, 1.00, "BEST", "d1"]
#el5 = [40, 50, 0.10, 0.25, 10, 5, 50, 1.00, "BEST", "d2"]
#el6 = [40, 50, 0.25, 0.10, 50, 5, 75, 1.00, "BEST", "d3"]
# Elite for Random instances
el7 = [20, 50, 0.50, 0.25, 25, 5, 75, 1.00, "FIRST-BEST", "d1"]
el8 = [60, 75, 0.50, 0.10, 100, 5, 75, 1.00, "FIRST-BEST", "d2"]
el9 = [40, 75, 0.25, 0.10, 75, 5, 75, 0.75 , "FIRST-BEST", "d3"]
el10 = [40, 50, 0.50, 0.10, 100, 5, 75, 0.75, "BEST", "d1"]
el11 = [40, 50, 0.25, 0.10, 10, 5, 75, 0.75, "BEST", "d2"]
el12 = [20, 50, 0.50, 0.10, 100, 5, 75, 0.75, "BEST", "d3"]



# Neare Elite Configurations
ne1 = [20, 50, 0.50, 0.10, 3, 3, 100, 0.50]
ne2 = [40, 75, 0.25, 0.10, 5, 3, 20, 0.75]
ne3 = [60, 50, 0.10, 0.10, 60, 7, 60, 0.75]
ne4 = [80, 100, 0.50, 0.10, 10, 5, 20, 1.00]
ne5 = [20, 50, 0.75, 0.10, 20, 20, 60, 0.75]
#ne6 = [60, 50, 0.50, 0.25, 5, 7, 60, 1.00]
#ne7 = [60, 10, 0.25, 1.00, 1, 5, 100, 0.75]
#ne8 = [40, 50, 0.50, 0.10, 40, 7, 100, 0.75]
#ne9 = [20, 50, 0.50, 0.10, 10, 5, 60, 1.00]
#ne10 = [60, 75, 0.50, 0.10, 3, 5, 60, 0.75]

#allConfigurations = [(rd1, "rd1"), (rd2, "rd2"), (rd3, "rd3"), (rd4, "rd4"), (rd5, "rd5"), (rd6, "rd6"), (rd7, "rd7"), (el1, "el1"), (el2, "el2"), (el3, "el3"), (el4, "el4"), (el5, "el5"), (el6, "el6"), (el7, "el7"), (ne1, "ne1"), (ne2, "ne2"), (ne3, "ne3"), (ne4, "ne4"), (ne5, "ne5"), (ne6, "ne6"), (ne7, "ne7")]
#allConfigurations = [(rd1, "rd1"), (rd2, "rd2"), (rd3, "rd3"), (rd4, "rd4"), (rd5, "rd5"), (el1, "el1"), (el2, "el2"), (el3, "el3"), (el4, "el4"), (el5, "el5")]
#allConfigurations += [(ne1, "ne1"), (ne2, "ne2"), (ne3, "ne3"), (ne4, "ne4"), (ne5, "ne5")]
allConfigurations = [(el7, "el7"), (el8, "el8"), (el9, "el9"), (el10, "el10"), (el11, "el11"), (el12, "el12")]

def call_script(args):
    subprocess.check_call(['python3', 'experiments_vrptw.py'] + args) 


def generate_neighborhood_configuration(configuration):
    neighborsConfiguration = [(configuration, "_base")]
    for i in range(10):
        name = namesParameters[i]
        #if name == "maximumSizePattern": # generate only configurations related to those parameters
        for param in allParameters[i]:
            newConfig = configuration.copy()
            if newConfig[i] != param:
                newConfig[i] = param
                neighborsConfiguration.append((newConfig, "_" + name + "_" + str(param)))
            
    return neighborsConfiguration

nameAlgo = "learning"
benchmark = "Generated"
run = "1"
sizeInstance = "100"
timeLimit = "720"
#metric = "d2"
#strategy = "FIRST-BEST"
probabilityMutation = "0.0"
operatorStrategy = "1"
seed = "1"


allArgs = []
for config, name in allConfigurations:
    #print(config)
    neighbours = generate_neighborhood_configuration(config)
    #print("Number of neighbours: ",len(neighbours))
    for testConfig,nameConfig in neighbours:
        if testConfig[4] == 1:
            nbGroups = 1
        else:
            nbGroups = int(testConfig[0] * testConfig[4]/100)
        for instanceID in id_instances:
            for instanceType in type_instances:
                listOfArgs = []
                listOfArgs.append(nameAlgo)
                listOfArgs.append(seed)
                listOfArgs.append(benchmark)
                intermediateSubpath = os.path.join(name, "Config" + nameConfig)
                listOfArgs.append(intermediateSubpath) # position of the run parameter
                listOfArgs.append(instanceID)
                listOfArgs.append(instanceType)
                listOfArgs.append(sizeInstance)
                listOfArgs.append(timeLimit)
                listOfArgs.append(str(testConfig[0]))
                listOfArgs.append(str(testConfig[0]//4))
                listOfArgs.append(testConfig[9])
                listOfArgs.append(str(testConfig[1]))
                listOfArgs.append(testConfig[8])
                listOfArgs.append(str(testConfig[2]))
                listOfArgs.append(probabilityMutation)
                listOfArgs.append(str(testConfig[3]))
                listOfArgs.append(str(nbGroups))
                listOfArgs.append(str(testConfig[5]))
                listOfArgs.append("standard")
                listOfArgs.append(operatorStrategy)
                listOfArgs.append(str(testConfig[6]))
                listOfArgs.append(str(testConfig[7]))
                listOfArgs.append(operatorStrategy)
                allArgs.append(listOfArgs)

for args in allArgs:
    subprocess.call(["sbatch", "--partition=2x24", "generate_jobs_basic.sh"] + args)
