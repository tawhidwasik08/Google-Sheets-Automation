# incrontab - tables for driving inotify cron (incron)
# resource: https://www.linux.com/topic/desktop/how-use-incron-monitor-important-files-and-folders/

# to add user
nano /etc/incron.allow

#add (after root is added, same for other users)
root

# configurations

incrontab -e

/home/maria/Desktop/Suspect/Codes/Google_Sheet_Automation/data/ IN_CREATE,IN_MOVED /home/maria/Desktop/Suspect/Codes/Google_Sheet_Automation/bash/update_shell.sh
