#!/bin/bash
module load anaconda3
module load parallel
source activate neutScriptsEnv

echo 'Extracting cells from TIFF images...'
arr=(./../images/*)
parallel python 'cellIsolation.py' ::: "${arr[@]}"

echo 'Analysing isolated cells...'
arrr=(./../cells/*)
parallel python 'nucAnalysis.py' ::: "${arrr[@]}"

echo 'Generating output summaries...'
python 'makeCSVs.py'
python 'makeGraphs.py'