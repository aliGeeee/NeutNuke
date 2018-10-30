module load anaconda3
module load parallel
source activate neutScriptsEnv

arr=(./../images/*)
parallel python cellIsolation.py ::: "${arr[@]}"

arrr=(./../cells/*)
parallel python nucAnalysis.py ::: "${arrr[@]}"