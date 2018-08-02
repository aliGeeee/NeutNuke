module load anaconda3
module load parallel
source activate neutScriptsEnv

arr=(./images/*)
chmod +x ./cellIsolation2.sh
parallel ./cellIsolation2.sh ::: "${arr[@]}"