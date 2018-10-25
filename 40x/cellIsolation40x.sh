module load anaconda3
module load parallel
source activate neutScriptsEnv

arr=(./images/*)
parallel python cellIsolation40x.py ::: "${arr[@]}"