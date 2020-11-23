import time 
import amazonMain
import signal
import sys
import time 
import calendar;
from datetime import datetime

def launchMain():
	amazonMain.main()

def closeDriver():
	amazonMain.closeDriver()

def update():
    times=0
    while True:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        times=times+1
        print("launching... ", times, dt_string)
        launchMain()
        print("launched!! at: ", dt_string, " going to sleep 1800sec")
        time.sleep(1800)


if __name__ == '__main__':
    update()
