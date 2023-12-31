from concurrent.futures import process
import os
import subprocess
from multiprocessing import Pool

def call_script(args):
    print(args)
    algo, benchmark, run, number, typ, size, time = args
    subprocess.check_call(['./generate_jobs_ITOR2023.sh', algo, benchmark, run, number, typ, size, time]) 

BENCHMARK = "Solomon"
ID_RUNS = [1,1] # format [start, end] where the id of the first (resp. last) run is start (resp. end)
SIZES_INSTANCE = [100]
TIME_LIMIT = [720]
NUMBER_CORES = 1
NAME_ALGORITHMS = ["fbd1"]
id_instances = {}

if BENCHMARK == "Solomon":
    # Solomon
    id_instances_C = ['101', '102', '103', '104', '105', '106', '107', '108', '109', '201', '202', '203', '204', '205', '206', '207', '208']
    id_instances_R = ['101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '201', '202', '203', '204', '205', '206', '207', '208', '209', '210', '211']
    id_instances_RC = ['101', '102', '103', '104', '105', '106', '107', '108', '201', '202', '203', '204', '205', '206', '207', '208']
	
    id_instances['C'] = id_instances_C
    id_instances['R'] = ['101'] #id_instances_R
    id_instances['RC'] = id_instances_RC

    type_instances = ['R']
    #id_instances['C'] = ["105"] #['101', '102', '201', '202']
    

elif BENCHMARK == "Generated":
    # Generated
    idInstances = ['1', '2', '3', '4', '5', '6', '7', '8']
    type_instances = []
    l1 = ['C', 'M', 'R']
    l2 = ['S', 'L']
    l3 = ['T', 'W']
    for a in l1:
        for b in l2:
            for c in l3:
                type_instances.append(a+b+c)
                id_instances[a+b+c] = idInstances
    type_instances = ["RLW"]
    id_instances["RLW"] = ['8']

elif BENCHMARK == "Homberger":
    # Homberger
    idInstances = [str(i) for i in range(1,2)]
    type_instances = ["R1_2_", "R2_2_", "C1_2_", "C2_2_"]

    for t in type_instances:
        id_instances[t] = idInstances

allArgs = []
for TYPE in type_instances:
    for NUMBER in id_instances[TYPE]:
        for RUN in range(ID_RUNS[0], ID_RUNS[1]+1):
        	for (s,t) in zip(SIZES_INSTANCE, TIME_LIMIT):
        		for algo in NAME_ALGORITHMS:
	            		allArgs.append([algo, BENCHMARK, str(RUN), NUMBER, TYPE, str(s), str(t)])
      				#subprocess.call(['sbatch', '--partition=2x12', 'generate_jobs_ITOR2023.sh', algo, BENCHMARK, str(RUN), NUMBER, TYPE, str(s), str(t)])

with Pool(processes= NUMBER_CORES) as pool:
    pool.map(call_script, allArgs)
