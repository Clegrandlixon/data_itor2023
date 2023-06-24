#echo "fbd1 C"
#irace -s scenario_C.txt -p parameters_ITOR2023.txt --log-file eliteConfigurations/fbd1/irace_fbd1_C.Rdata --target-runner runners/target_runner_fbd1.py --target-evaluator evaluators/target_evaluator_fbd1.py > eliteConfigurations/fbd1/execution_fbd1_C.txt

#echo "fbd2 C"
#irace -s scenario_C.txt -p parameters_ITOR2023.txt --log-file eliteConfigurations/fbd2/irace_fbd2_C.Rdata --target-runner runners/target_runner_fbd2.py --target-evaluator evaluators/target_evaluator_fbd2.py > eliteConfigurations/fbd2/execution_fbd2_C.txt

#echo "fbd3 C"
#irace -s scenario_C.txt -p parameters_ITOR2023.txt --log-file eliteConfigurations/fbd3/irace_fbd3_C.Rdata --target-runner runners/target_runner_fbd3.py --target-evaluator evaluators/target_evaluator_fbd3.py > eliteConfigurations/fbd3/execution_fbd3_C.txt

#echo "bd1 C"
#irace -s scenario_C.txt -p parameters_ITOR2023.txt --log-file eliteConfigurations/bd1/irace_bd1_C.Rdata --target-runner runners/target_runner_bd1.py --target-evaluator evaluators/target_evaluator_bd1.py > eliteConfigurations/bd1/execution_bd1_C.txt

#echo "bd2 C"
#irace -s scenario_C.txt -p parameters_ITOR2023.txt --log-file eliteConfigurations/bd2/irace_bd2_C.Rdata --target-runner runners/target_runner_bd2.py --target-evaluator evaluators/target_evaluator_bd2.py > eliteConfigurations/bd2/execution_bd2_C.txt

#echo "bd3 C"
#irace -s scenario_C.txt -p parameters_ITOR2023.txt --log-file eliteConfigurations/bd3/irace_bd3_C.Rdata --target-runner runners/target_runner_bd3.py --target-evaluator evaluators/target_evaluator_bd3.py > eliteConfigurations/bd3/execution_bd3_C.txt

#echo "moead C"
#irace -s scenario_C.txt -p parameters_ITOR2023_noLearning.txt --log-file eliteConfigurations/moeadls/irace_moead_C.Rdata --target-runner runners/target_runner_moead.py --target-evaluator evaluators/target_evaluator_moead.py > eliteConfigurations/moeadls/execution_moead_C.txt

echo "hmoead C"
irace -s scenario_C.txt -p parameters_ITOR2023.txt --log-file eliteConfigurations/hmoead/irace_hmoead_C.Rdata --target-runner runners/target_runner_hmoead.py --target-evaluator evaluators/target_evaluator_hmoead.py > eliteConfigurations/hmoead/execution_hmoead_C.txt

# Random instances
#echo "fbd1 R"
#irace -s scenario_R.txt -p parameters_ITOR2023.txt --log-file eliteConfigurations/fbd1/irace_fbd1_R.Rdata --target-runner runners/target_runner_fbd1.py --target-evaluator evaluators/target_evaluator_fbd1.py > eliteConfigurations/fbd1/execution_fbd1_R.txt

#echo "fbd2 R"
#irace -s scenario_R.txt -p parameters_ITOR2023.txt --log-file eliteConfigurations/fbd2/irace_fbd2_R.Rdata --target-runner runners/target_runner_fbd2.py --target-evaluator evaluators/target_evaluator_fbd2.py > eliteConfigurations/fbd2/execution_fbd2_R.txt

#echo "fbd3 R"
#irace -s scenario_R.txt -p parameters_ITOR2023.txt --log-file eliteConfigurations/fbd3/irace_fbd3_R.Rdata --target-runner runners/target_runner_fbd3.py --target-evaluator evaluators/target_evaluator_fbd3.py > eliteConfigurations/fbd3/execution_fbd3_R.txt

#echo "bd1 R"
#irace -s scenario_R.txt -p parameters_ITOR2023.txt --log-file eliteConfigurations/bd1/irace_bd1_R.Rdata --target-runner runners/target_runner_bd1.py --target-evaluator evaluators/target_evaluator_bd1.py > eliteConfigurations/bd1/execution_bd1_R.txt

#echo "bd2 R"
#irace -s scenario_R.txt -p parameters_ITOR2023.txt --log-file eliteConfigurations/bd2/irace_bd2_R.Rdata --target-runner runners/target_runner_bd2.py --target-evaluator evaluators/target_evaluator_bd2.py > eliteConfigurations/bd2/execution_bd2_R.txt

#echo "bd3 R"
#irace -s scenario_R.txt -p parameters_ITOR2023.txt --log-file eliteConfigurations/bd3/irace_bd3_R.Rdata --target-runner runners/target_runner_bd3.py --target-evaluator evaluators/target_evaluator_bd3.py > eliteConfigurations/bd3/execution_bd3_R.txt

#echo "moead R"
#irace -s scenario_R.txt -p parameters_ITOR2023_noLearning.txt --log-file eliteConfigurations/moeadls/irace_moead_R.Rdata --target-runner runners/target_runner_moead.py --target-evaluator evaluators/target_evaluator_moead.py > eliteConfigurations/moeadls/execution_moead_R.txt

echo "hmoead R"
irace -s scenario_R.txt -p parameters_ITOR2023.txt --log-file eliteConfigurations/hmoead/irace_hmoead_R.Rdata --target-runner runners/target_runner_hmoead.py --target-evaluator evaluators/target_evaluator_hmoead.py > eliteConfigurations/hmoead/execution_hmoead_R.txt
