import time 
import amazonMain


def update():
    times=0
    while True:
        times=times+1
        print("launching... ", times)
        amazonMain.main()
        print("launched!! going to sleep 7200sec")
        time.sleep(3600)


if __name__ == '__main__':
    update()
