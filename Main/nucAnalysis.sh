module load anaconda3
module load parallel
source activate neutScriptsEnv

arr=(./cells/*)
parallel python nucAnalysis2.py ::: "${arr[@]}"