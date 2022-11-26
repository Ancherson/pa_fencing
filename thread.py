from threading import Lock
from threading import Thread
import threading
lock = Lock()
alarm_clock = threading.Event()
i = 0
y=0

def task():
    for _ in range(100000):
        lock.acquire()
        global i
        i+= 1 
        lock.release()
    print('done')

def task2():
    for _ in range(100000):
        alarm_clock.wait()
        lock.acquire()
        global y
        y+= 1 
        lock.release()
    print('done')
# create two new threads
t1 = Thread(target=task)
t2 = Thread(target=task)

# start the threads
t1.start()
t2.start()


threads = []
alarm_clock.clear()
for j in range(10):
    print(f"thread {j} launched")
    thread = Thread(target=task2)
    threads.append(thread)
    thread.start()
    
print(threading.active_count())
print(y)

alarm_clock.set()
for th in threads:
    th.join()
print(y)