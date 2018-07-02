#http://stackoverflow.com/questions/16199793/python-3-3-simple-threading-event-example

#!python3
import threading, os, io, datetime
from queue import Queue
import time

THREAD_POOL = 4
FILESHARE = r'\\ccluatsblapp1\ADMIN\Integration\DataSync'
SERVERNAME = 'CCLTSTSBLSQL1'
DBNAME = 'SIEBELDB'
TABLENAME = 'tblCBICSiebelSync_STG'
WORKFOLDER = r'D:\TEMP'
LOGFILE = WORKFOLDER + '\\logfile.out'
DICT_RESULTS = {}

#===============FUNCTIONS==================================================================
def ScrubFile(filein, fileout, strtoremove):
    '''
    Cleans input file line by line
    '''
    lines = 0
    #outfile = open(fileout, 'wt',encoding="ascii", errors="surrogateescape", newline='\n')
    outfile = open(fileout, 'wt',encoding="ascii")
    s = ''
    with open(filein, 'rt', encoding="ascii", errors="surrogateescape", newline='\n') as infile:
        for x in infile:
            try:
                if x[0] == "'": x = x[1:]
                if x[-1] == "'": x = x[:-1]
                x = x.replace("','", ",")
                x = x.replace(",'", ",")
                x = x.replace("',", ",")
                outfile.write(x)
            except UnicodeEncodeError:
                s = s + '\n' + x
                pass

            lines = lines + 1
    outfile.close()
    return lines, s

#===============End of functions===========================================================

#exit()


#(bcp tblCBICSiebelSync in $fixedfile -f $WORKFOLDER\Person_Push.fmt -S $SERVERNAME -d SIEBELDB -T)
#(bcp tblCBICSiebelSync_STG in $fixedfile -f $WORKFOLDER\Person_Push.fmt -S $SERVERNAME -d SIEBELDB -T -L 100)

#for testing with one file
#filelist = ['person_sbl_push_group_01.csv']
filelist = os.listdir(FILESHARE)

#test: using only 2 files
filelist = filelist[:2]

print('list of files: ', filelist, len(filelist))

#outfile = open(r'd:\temp\threading.out', 'w')

# lock to serialize console output
lock = threading.Lock()

def get_next_file(filelist):
    try:
        item = filelist.pop()
    except IndexError:
        item = -1
    return item



def do_work(item):
    #do some lengthy work.
    f = get_next_file(filelist)
    if f != -1:
        now1 = datetime.datetime.now()
        #for testing with small file
        #curr_file = WORKFOLDER + '\\' + f
        curr_file = FILESHARE + '\\' + f

        # put here the actual work to be done
        fileout = curr_file.replace(".csv", ".out")         #changing file name
        fileout = fileout.replace(FILESHARE, WORKFOLDER)
        lines, errs = ScrubFile(curr_file, fileout, "'")
        s = "bcp " + TABLENAME + " in " + fileout + " -f " + WORKFOLDER + '\\Person_Push.fmt -S ' + SERVERNAME + ' -d'  + DBNAME + " -T -L 100"

        #print(s)
        #print(os.path.exists(curr_file), curr_file)
        # Make sure the whole print completes or threads can mix up output in one line.
        DICT_RESULTS[threading.current_thread().name].append(f)
        with lock:
            print(os.path.exists(curr_file), curr_file)
            print('lines=', lines)
            #print('error lines: ', errs)
            #with open(filein, 'rt', encoding="ascii", errors="surrogateescape", newline='\n') as infile:
            with open(LOGFILE, 'at', encoding="ascii", errors="surrogateescape", newline='\n') as thelogfile:
                thelogfile.write(curr_file + '\n')
                thelogfile.write('lines:\n' )
                thelogfile.write(str(lines) + '\n')
                thelogfile.write(errs + '\n')
                now2 = datetime.datetime.now()
                thelogfile.write('time to process file:')
                thelogfile.write(str(now2-now1))
                thelogfile.write("\n\n")
                thelogfile.close()




            #print(threading.current_thread().name,item, f)



# The worker thread pulls an item from the queue and processes it
def worker():
    while True:
        item = q.get()
        do_work(item)
        q.task_done()

# Create the queue and thread pool.
q = Queue()
for i in range(THREAD_POOL):
     t = threading.Thread(target=worker)
     DICT_RESULTS[t.name] = []
     t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
     t.start()


# stuff work items on the queue.
start = time.perf_counter()         #saving start time
for item in range(len(filelist)):
    q.put(item)


q.join()       # block until all tasks are done


# "Work" took .1 seconds per task.
# 20 tasks serially would be 2 seconds.
# With 4 threads should be about .5 seconds (contrived because non-CPU intensive "work")
print('time:',time.perf_counter() - start)
#print (DICT_RESULTS)
for x in sorted(DICT_RESULTS.keys()):
    print(x,DICT_RESULTS[x])