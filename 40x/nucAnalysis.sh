module load anaconda3
module load parallel
source activate neutScriptsEnv

arr=(./cells/*)
parallel python nucAnalysis.py ::: "${arr[@]}"