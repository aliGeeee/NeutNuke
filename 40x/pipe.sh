module load anaconda3
module load parallel
source activate neutScriptsEnv

arr=(./images/*)
parallel python cellIsolation40x.py ::: "${arr[@]}"

python groupAnnotations.py

arrr=(./cells/*)
parallel python nucAnalysis.py ::: "${arrr[@]}"