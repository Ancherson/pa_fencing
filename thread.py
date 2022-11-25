from time import sleep, perf_counter
from threading import Thread


def task():
    for i in range(10):
        sleep(1)
        print(i)
    print('done')


# create two new threads
t1 = Thread(target=task)
t2 = Thread(target=task)

# start the threads
t1.start()
t2.start()


