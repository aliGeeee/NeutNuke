#!/bin/bash
(wget -O - pi.dk/3 || curl pi.dk/3/ || fetch -o - http://pi.dk/3) | bash
module load anaconda3
conda create --name neutScriptsEnv -y
source activate neutScriptsEnv
conda install python -y -q
conda install opencv -y -q
python -m pip install progress -q
python -m pip install matplotlib -q
python -m pip install pandas -q
python -m pip install scipy -q
python -m pip install seaborn -q
source deactivate neutScriptsEnv
echo "Successfully created the environment 'neutScriptsEnv'"