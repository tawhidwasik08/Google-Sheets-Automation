#!/bin/bash

# variables
logfile_loc=/home/maria/Desktop/Suspect/Codes/Google_Sheet_Automation/log.out
conda_env_loc=~/anaconda3/etc/profile.d/conda.sh
conda_python_loc=~/anaconda3/envs/suspect/bin/python3
main_python_loc=~/Desktop/Suspect/Codes/Google_Sheet_Automation/gsheet_automation/main.py


# logging (reference: https://serverfault.com/a/103569)
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>> $logfile_loc 2>&1


# activate conda environment
source $conda_env_loc
conda activate suspect

echo Time: `date`
# checking current conda environment
echo -e "conda env: $CONDA_DEFAULT_ENV"

echo -e "Output:"


# run update script
$conda_python_loc $main_python_loc
echo -e "======================================================================"

