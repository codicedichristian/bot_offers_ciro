import threading
import time 
import amazonMain

def update():
    while True:
        amazonMain.main()
        print("launched")
        time.sleep(7200)


if __name__ == '__main__':
    update()
