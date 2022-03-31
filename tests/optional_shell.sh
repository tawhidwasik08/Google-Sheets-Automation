#! /usr/bin/bash
# activate conda environment
source ~/anaconda3/etc/profile.d/conda.sh
conda activate suspect

# checking current conda environment (suspect)
echo -e "\n-------->> Active environment: $CONDA_DEFAULT_ENV <<--------\n"

# read for different options
echo "1: for updating sheets with new data"
echo "2: for recreating all data (including new)"
echo -e "\n"

read -p 'Option: ' option

# run recreation or update python scripts
if [[ $option == "1" ]]
then
    python google_sheet_upload.py
else
    python google_sheet_upload.py -c
fi

