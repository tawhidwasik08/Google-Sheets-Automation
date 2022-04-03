# Google Sheets Automation
 [![HitCount](https://hits.dwyl.com/tawhidwasik08/https://githubcom/tawhidwasik08/Google-Sheets-Automation.svg?style=flat)](http://hits.dwyl.com/tawhidwasik08/https://githubcom/tawhidwasik08/Google-Sheets-Automation)
 
# A Little Explanation on The Project
This project is about quality of life improvement. For one of my projects in my job, there was a challange where we had to collect data from a CRM website daily for data visualiztion along with data from some other sources which wouldn't require any additional data storing. 

After spending some time in analysing the data, the frequency it being updated, I thought of using google sheets as a simple data storing solution. The project is all about automating the tasks of cleaning the data and uploading the new data in google sheets.

# How does it work ?
The source mentioned above is google recaptha v3 protected. So, a scraping script was inconsistent. In the end the pipeline just became,
1. Downloading new `.csv` dataset from the source into a set destination folder.
2. The folder is always being monitored by `incron` daemon. As soon as a new file is moved/downloaded here it excutes a `.shell` file.
3. The shell file sets up right conda environment, starts keeping log and executes a python script.
4. The python scripts checks all files in the folder. If a newer file is found:
    - Cleans it
    - Checks existing google sheet primary key column
    - If newer primary keys are foumd, updates the google sheets with new rows

# Project structure
```
Google Sheets Automation
├── data
│   ├── dataset.csv
│   ├── secrets.json
│   └── google_service_auth_info.json
├── gsheet_automation
│   ├── main.py
│   ├── update_shell.sh
│   └── utilities.py
├── log.out
├── README.md
├── requirements.yml
└── tests
    ├── optional_shell.sh
    └── regex_test.py
```
# Getting Started
Follow along [this](https://www.youtube.com/watch?v=bu5wXjz2KvU) to find how to set up and get `google_service_auth_info.json`

Create a new conda environment from requirements.yml file.
```sh 
conda env create -f environment.yml
```
Update the location variables in `gsheet_automation/update_shell.sh` accordingly

Install incron by issuing the command the following command in terminal
```sh 
sudo apt-get install incron
```

Specify who can use [`incron`](https://www.linux.com/topic/desktop/how-use-incron-monitor-important-files-and-folders/). Add root and any other user names in the following file.
```sh
sudo -u root nano /etc/incron
```
Then, 
```sh
incrontab -e
```
Add `<monitored_dir> <mask>,<mask> <path_of_bash> <executable_shell>`
```sh
/absolute_path.../Google_Sheet_Automation/data/ IN_CREATE,IN_MOVED /bin/bash /absolute_path.../Google_Sheet_Automation/gsheet_automation/update_shell.sh
```

## For obvious privacy reasons no data was uploaded