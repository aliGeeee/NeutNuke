module load anaconda3
conda create --name neutScriptsEnv -y
source activate neutScriptsEnv
conda install opencv -y
python -m pip install progress
python -m pip install matplotlib
python -m pip install pandas
source deactivate neutScriptsEnv