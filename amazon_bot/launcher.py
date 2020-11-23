import time 
import amazonMain
import signal
import sys
import time 
import calendar;

def update():
    times=0
    while True:
        times=times+1
        ts = calendar.timegm(time.gmtime())
        print("launching... ", times)
        amazonMain.main()
        print("launched!! at: ", ts, " going to sleep 1800sec")
        time.sleep(1800)


if __name__ == '__main__':
    update()
