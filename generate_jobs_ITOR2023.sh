#!/bin/bash

#SBATCH --partition=2x24
#SBATCH --job-name=hostname
#SBATCH --output=slurm.out
#SBATCH --error=slurm.err

### Arguments to specify from left to right

# Option: -k (--printKnowledge): display the content of the knowledge groups after the execution
#    	  -f (--useReferenceFront): use the reference front stored in the file ""
# ($1) Name of the algorithm
# Seed
# ($2) Name of the Benchmark (either "Solomon" or "Generated")
# ($3) Id of the run
# ($4) Number of the instance (see the available instances)
# ($5) Type of instance (either C, R or RC for Solomon's instances)
# ($6) Size of the instance
# ($7) Termination criteron
# Size of the population (number of subproblems in MOEAD)
# Size of the neighborhood of a subproblem
# Metric used to measure the distance between two customers (either "d1", "d2" or "d3")
# Granularity (to prune the exploration space during the local search)
# Exploration strategy for the local search (either "FIRST-BEST" or "BEST-BEST")
# Probability of Crossover
# Probability of Mutation
# Probability of Local Search
# Number of Groups
# Maximum size of patterns extracted
# Solutions used for extraction (for now only "standard" is available)
# Extraction strategy
# Number of patterns injected
# Probability of injection
# Injection strategy


# Check the file experiments_vrptw.py to see how the algorithm is built

case $1 in

    fbd1)	
	case $5 in
	    C)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 100 $7 40 10 "d1" 50 "FIRST-BEST" 0.50 0.00 0.10 20 5 "standard" 1 100 0.75 1;;
	    R)
	    	python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 100 $7 40 10 "d1" 75 "FIRST-BEST" 0.50 0.00 0.10 20 8 "standard" 1 100 1.00 1;;
	    C1_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d1" 100 "FIRST-BEST" 0.50 0.00 0.10 20 5 "standard" 1 200 0.75 1;;
	    C2_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d1" 100 "FIRST-BEST" 0.50 0.00 0.10 20 5 "standard" 1 200 0.75 1;;
	    R1_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d1" 150 "FIRST-BEST" 0.50 0.00 0.10 20 8 "standard" 1 200 1.00 1;;
	    R2_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d1" 150 "FIRST-BEST" 0.50 0.00 0.10 20 8 "standard" 1 200 1.00 1;;
	esac;;

    fbd2)	
	case $5 in
	    C)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 100 $7 40 10 "d2" 50 "FIRST-BEST" 0.50 0.00 0.10 20 5 "standard" 1 100 1.00 1;;
	    R)
	    	python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 100 $7 40 10 "d2" 75 "FIRST-BEST" 0.50 0.00 0.20 10 8 "standard" 1 100 1.00 1;;
	    C1_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d2" 100 "FIRST-BEST" 0.50 0.00 0.10 20 5 "standard" 1 200 1.00 1;;
	    C2_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d2" 100 "FIRST-BEST" 0.50 0.00 0.10 20 5 "standard" 1 200 1.00 1;;
	    R1_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d2" 150 "FIRST-BEST" 0.50 0.00 0.20 10 8 "standard" 1 200 1.00 1;;
	    R2_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d2" 150 "FIRST-BEST" 0.50 0.00 0.20 10 8 "standard" 1 200 1.00 1;;
	esac;;
    
    fbd3)	
	case $5 in
	    C)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 100 $7 40 10 "d3" 50 "FIRST-BEST" 0.50 0.00 0.10 40 5 "standard" 1 100 1.00 1;;
	    R)
	    	python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 100 $7 40 10 "d3" 75 "FIRST-BEST" 0.50 0.00 0.10 20 8 "standard" 1 100 0.75 1;;
	    C1_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d3" 100 "FIRST-BEST" 0.50 0.00 0.10 40 5 "standard" 1 200 1.00 1;;
	    C2_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d3" 100 "FIRST-BEST" 0.50 0.00 0.10 40 5 "standard" 1 200 1.00 1;;
	    R1_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d3" 150 "FIRST-BEST" 0.50 0.00 0.10 20 8 "standard" 1 200 0.75 1;;
	    R2_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d3" 150 "FIRST-BEST" 0.50 0.00 0.10 20 8 "standard" 1 200 0.75 1;;
	esac;;

    bd1)	
	case $5 in
	    C)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 100 $7 40 10 "d1" 50 "BEST-BEST" 0.50 0.00 0.10 40 5 "standard" 1 100 1.00 1;;
	    R)
	    	python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 100 $7 40 10 "d1" 50 "BEST-BEST" 0.50 0.00 0.10 40 8 "standard" 1 100 0.75 1;;
	    C1_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d1" 100 "BEST-BEST" 0.50 0.00 0.10 40 5 "standard" 1 200 1.00 1;;
	    C2_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d1" 100 "BEST-BEST" 0.50 0.00 0.10 40 5 "standard" 1 200 1.00 1;;
	    R1_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d1" 100 "BEST-BEST" 0.50 0.00 0.10 40 8 "standard" 1 200 0.75 1;;
	    R2_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d1" 100 "BEST-BEST" 0.50 0.00 0.10 40 8 "standard" 1 200 0.75 1;;
	esac;;

    bd2)	
	case $5 in
	    C)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 100 $7 40 10 "d2" 50 "BEST-BEST" 0.50 0.00 0.10 40 2 "standard" 1 100 0.75 1;;
	    R)
	    	python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 100 $7 40 10 "d2" 50 "BEST-BEST" 0.50 0.00 0.10 40 8 "standard" 1 100 1.00 1;;
	    C1_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d2" 100 "BEST-BEST" 0.50 0.00 0.10 40 2 "standard" 1 200 0.75 1;;
	    C2_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d2" 100 "BEST-BEST" 0.50 0.00 0.10 40 2 "standard" 1 200 0.75 1;;
	    R1_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d2" 100 "BEST-BEST" 0.50 0.00 0.10 40 8 "standard" 1 200 1.00 1;;
	    R2_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d2" 100 "BEST-BEST" 0.50 0.00 0.10 40 8 "standard" 1 200 1.00 1;;
	esac;;

    bd3)	
	case $5 in
	    C)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 100 $7 40 10 "d3" 50 "BEST-BEST" 0.50 0.00 0.10 40 2 "standard" 1 100 0.75 1;;
	    R)
	    	python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 100 $7 40 10 "d3" 25 "BEST-BEST" 0.50 0.00 0.10 20 2 "standard" 1 100 0.75 1;;
	    C1_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d3" 100 "BEST-BEST" 0.50 0.00 0.10 40 2 "standard" 1 200 0.75 1;;
	    C2_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d3" 100 "BEST-BEST" 0.50 0.00 0.10 40 2 "standard" 1 200 0.75 1;;
	    R1_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d3" 50 "BEST-BEST" 0.50 0.00 0.10 20 2 "standard" 1 200 0.75 1;;
	    R2_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d3" 50 "BEST-BEST" 0.50 0.00 0.10 20 2 "standard" 1 200 0.75 1;;
	esac;;

    moeadls)
	case $5 in
	    C)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 100 $7 40 10 "d3" 50 "FIRST-BEST" 1.00 0.00 0.10 1 2 "standard" 1 1 0.00 1;;
	    R)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 100 $7 80 20 "d2" 75 "FIRST-BEST" 1.00 0.00 0.10 1 2 "standard" 1 1 0.00 1;;
	    C1_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d3" 100 "FIRST-BEST" 1.00 0.00 0.10 1 2 "standard" 1 1 0.00 1;;
	    C2_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 40 10 "d3" 100 "FIRST-BEST" 1.00 0.00 0.10 1 2 "standard" 1 1 0.00 1;;
	    R1_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 80 20 "d2" 150 "FIRST-BEST" 1.00 0.00 0.10 1 2 "standard" 1 1 0.00 1;;
	    R2_2_)
		python3 experiments_vrptw.py -f $1 1 $2 $3 $4 $5 200 $7 80 20 "d2" 150 "FIRST-BEST" 1.00 0.00 0.10 1 2 "standard" 1 1 0.00 1;;
	esac;;
    
esac
