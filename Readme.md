# Tuning
The tuning is performed with irace. If you have any question about it, please refer to the corresponding documentation.

- It is possible to run the tuning of the algorithm with the file tuning/run_irace.sh (by default only algorithm is selected, being hmoead. It is possible to uncomment other lines to tune other variants). The results are automatically stored in the eliteConfigurations/ folder. (do not forget to add the jmetal folder to the folders runners/ and evaluators/)
- The elite configurations we obtained are stored in tuning/eliteConfigurations_final. It also contains the logfiles of irace.

# Performances
The code is in jmetal/ (tested for python 3.8)

- It is possible to run the algorithm by using the file run_jobs.py. In this file, it is possible to modify the instances used, the number of runs, and the time allocated to a run.
- The results are automatically stored in a data/ folder (created if it does not exist).
- The results we obtained are already stored in performance_results/files.zip.
- The files fronts.py and generate_tables.py are useful to post-process the data obtained before runing statistical analysis in R. (do not forget to unzip files.zip before using them).

# Resources
- Instances are stored in resources/VRPTW_instances
- Reference fronts are available in resources/reference_front
- The reference fronts used during our experiments are stored in resources/reference_fronts_forExperiments. They might slightly differ from those stored in reference_front.
- Additional data concerning the instances can be found in Results/.../table.tsv

# Contact information
For any request, please feel free to contact me at: clement.legrand4.etu@univ-lille.fr

