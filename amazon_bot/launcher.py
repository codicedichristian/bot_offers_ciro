import time 
import amazonMain
import signal
import sys

def update():
    times=0
    while True:
        times=times+1
        print("launching... ", times)
        amazonMain.main()
        print("launched!! going to sleep 1800sec")
        time.sleep(1800)


if __name__ == '__main__':
    update()
