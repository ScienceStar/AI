import threading
import time
from concurrent.futures import ThreadPoolExecutor

def task(i):
    print(i)

with ThreadPoolExecutor(max_workers=5) as pool:
    pool.map(task, range(10))

class MyThread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print(self.name, "running")
        time.sleep(1)

t = MyThread("t1")
t.start()


def worker(name):
    print(f"{name} start")
    time.sleep(2)
    print(f"{name} end")

t1 = threading.Thread(target=worker, args=("thread-1",))
t2 = threading.Thread(target=worker, args=("thread-2",))

t1.start()
t2.start()

t1.join()
t2.join()

print("main thread end")