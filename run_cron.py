import os
from time import sleep
time_sleep = 60*60*24
while True:
    print("sleep",time_sleep)
    sleep(time_sleep)
    os.system("python cron.py")
    