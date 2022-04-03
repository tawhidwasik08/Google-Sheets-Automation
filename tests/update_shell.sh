#!/bin/bash
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>/home/maria/Desktop/Suspect/Codes/Google_Sheet_Automation/log.out 2>&1
# activate conda environment
source ~/anaconda3/etc/profile.d/conda.sh
conda activate suspect

# checking current conda environment
echo -e "\n-------->> Active environment: $CONDA_DEFAULT_ENV <<--------\n"


# moving/creating file takes a time i guess ? try sleep

# run update script
~/anaconda3/envs/suspect/bin/python3 ~/Desktop/Suspect/Codes/Google_Sheet_Automation/google_sheet_upload.py
