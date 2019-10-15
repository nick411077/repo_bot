from threading import Event, Thread
from time import sleep

singal = Event()


def func(singal):
    while True:
        singal.wait()  # wait for singal turn on
        print("do job")
        print("job end")
        singal.clear()  # turn off singal


t = Thread(target=func, args=[singal])
t.start()

print("1st time")
singal.set()  # turn on singal
sleep(3)

print("2nd time")
singal.set()
sleep(3)

print("3rd time")
singal.set()
sleep(3)
