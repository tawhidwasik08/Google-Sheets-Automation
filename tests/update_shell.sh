#! /usr/bin/bash
# activate conda environment
source ~/anaconda3/etc/profile.d/conda.sh
conda activate suspect

# checking current conda environment (suspect)
echo -e "\n-------->> Active environment: $CONDA_DEFAULT_ENV <<--------\n"

# run update script
python google_sheet_upload.py
