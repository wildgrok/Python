__author__ = 'jorgebe'


#!python3
import threading, os
from queue import Queue
import time


FILESHARE = r'\\ccluatsblapp1\ADMIN\Integration\DataSync'

#(bcp tblCBICSiebelSync in $fixedfile -f $WORKFOLDER\Person_Push.fmt -S $SERVERNAME -d SIEBELDB -T)

filelist = os.listdir(FILESHARE)
print('list of files: ', filelist)

outfile = open(r'd:\temp\threading.out', 'w')

# lock to serialize console output
lock = threading.Lock()

def get_next_file(filelist):
    try:
        item = filelist.pop()
    except IndexError:
        item = -1
    return item



def do_work(item):
    #time.sleep(.1) # pretend to do some lengthy work.
    
    if get_next_file(filelist) != -1:
        curr_file = FILESHARE + '\\' + get_next_file(filelist)
        print(os.path.exists(curr_file), curr_file)
    #outfile.write(str(lst))
    # Make sure the whole print completes or threads can mix up output in one line.
        with lock:
            print(threading.current_thread().name,item)

# The worker thread pulls an item from the queue and processes it
def worker():
    while True:
        item = q.get()
        do_work(item)
        q.task_done()

# Create the queue and thread pool.
q = Queue()
for i in range(4):
     t = threading.Thread(target=worker)
     t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
     t.start()

# stuff work items on the queue (in this case, just a number).
start = time.perf_counter()
for item in range(40):
    q.put(item)

# for item in range(20):
#q.put(item)

q.join()       # block until all tasks are done
outfile.close()

# "Work" took .1 seconds per task.
# 20 tasks serially would be 2 seconds.
# With 4 threads should be about .5 seconds (contrived because non-CPU intensive "work")
print('time:',time.perf_counter() - start)