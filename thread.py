from threading import Lock
from threading import Thread
lock = Lock()

i = 0


def task():
    for _ in range(100000):
        lock.acquire()
        global i
        i+= 1 
        lock.release()
    print('done')


# create two new threads
t1 = Thread(target=task)
t2 = Thread(target=task)

# start the threads
t1.start()
t2.start()

t1.join()
t2.join()
print(i)
