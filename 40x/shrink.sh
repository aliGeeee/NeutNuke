module load anaconda3
module load parallel
source activate neutScriptsEnv

arr=(./allCells/*)
parallel python shrink.py ::: "${arr[@]}"