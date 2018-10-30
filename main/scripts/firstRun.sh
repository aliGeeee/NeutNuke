module load anaconda3
conda create --name neutScriptsEnv -y
source activate neutScriptsEnv
conda install python -y -q
conda install opencv -y -q
python -m pip install progress -q
python -m pip install matplotlib -q
python -m pip install pandas -q
python -m pip install scipy -q
source deactivate neutScriptsEnv
echo "Successfully created the environment 'neutScriptsEnv'"