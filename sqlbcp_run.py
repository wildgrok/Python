# version in HP PC at work

from sqlbcp import *
import time
import threading
import queue
DICT_RESULTS2 = []
# 0 means will process all entries in its own thread
THREAD_POOL = 5
NOEXECUTE_OPTION = 0


# --------------------------threading functions---------------------------------


def do_work(item):
    """
    do lengthy work
    """
    start2 = time.perf_counter()            # saving start time
    line = dct.popitem()                    # dct contains all the bcp entries in tablename/bcp line pairs
    table = line[0]
    bcpitem = line[1]
    # for testing
    if NOEXECUTE_OPTION == 0:
        output = runbcp(bcpitem)
    else:
        output = bcpitem
    DICT_RESULTS = {}  # storage for item run data
    ThreadItem = threading.current_thread().name + '_' + str(item)
    DICT_RESULTS[ThreadItem] = {}
    DICT_RESULTS[ThreadItem]['table processed:'] = table
    DICT_RESULTS[ThreadItem]['table output:'] = output

    time_elapsed = time.perf_counter() - start2
    DICT_RESULTS[ThreadItem]['ELAPSED TIME'] = time_elapsed
    DICT_RESULTS2.append(DICT_RESULTS)


def worker():
    """
    The worker thread pulls an item from the queue and processes it
    """
    while True:
        item = q.get()
        do_work(item)
        q.task_done()

# --------------end of threading functions--------------

# def BcpOneDB(CONNECTION, database, DATAFOLDER, action, opt):
#     bcpobj = sqlbcp(CONNECTION, database, DATAFOLDER, 'out', [], [], opt)
#     dct = bcpobj.bcp()
#     LogBCP(CONNECTION, database, dct)
#     print('deleting all rows in destination database (for testing re-runs)')
#     if action == 'in':
#         res, lst = Delete_from_all_tables(CONNECTION, database)
#         if res is True:
#             print('all records deleted')
#         else:
#             print('deletion not successful')
#             for x in lst:
#                 print(x)
#
#     print('-------------doing threaded bcp in--------------------------')
#     items_to_process = len(dct)
#     # Using a default of 5 threads if pool not specified
#     if THREAD_POOL == 0:
#         THREAD_POOL = int(items_to_process / 5)
#     print('Total items to process:', items_to_process)
#     print('Thread pool (concurrent processes): ', THREAD_POOL)
#     if NOEXECUTE_OPTION == 0:
#         print('Execution option is yes')
#     else:
#         print('No execution')
#     # Threading starts from here on: we have the dictionary with all the bcps
#     # lock to serialize console output
#     lock = threading.Lock()
#
#     # Create the queue and thread pool.
#     q = queue.Queue()
#     for i in range(THREAD_POOL):
#         t = threading.Thread(target=worker)
#         t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
#         t.start()
#
#     # stuff work items on the queue.
#     start1 = time.perf_counter()         # saving start time
#     for item in range(len(dct)):
#         q.put(item)
#         time.sleep(0.05)
#
#     q.join()
#
#     print('time:', time.perf_counter() - start1)
#     print('displaying results')
#     for x in DICT_RESULTS2:
#         print(x)
#     # end of function BcpOneDB

#
# CONNECTION = {}
# SQLSERVER = r'(local)\sql2014'
# CONNECTION['servername'] = SQLSERVER
# CONNECTION['username'] = ''
# CONNECTION['password'] = ''
# database = 'AdventureWorks2012'
# print('Connection dict:', CONNECTION)
# DATAFOLDER = r'd:\temp'
# action = 'out'
# opt = {'ext': '.bin', 'auto_db_folders': False}
# BcpOneDB(CONNECTION, database, DATAFOLDER, action, opt)
#
#
#
# exit()

# --------------Program start---------------------------

# SQLSERVER = r'(local)\sql2014'
# CONNECTION['servername'] = SQLSERVER
# CONNECTION['username'] = ''
# CONNECTION['password'] = ''
# database = 'AdventureWorks2012'
# print('Connection dict:', CONNECTION)
# DATAFOLDER = r'd:\temp'
# opt = {'ext': '.bin', 'auto_db_folders': True}


# print('-------------------testing select query-----------------------')
# rows, fnames = SqlExecute(CONNECTION, 'set nocount on select top 10  * from AdventureWorks2012.Person.Person')
# print(fnames)
# for x in rows:
#     print(x)
# exit()

# print('------------test of list datafiles-----------------------------')
# a = GetFiles(DATAFOLDER + r'\AdventureWorks2012', '.bin')
# for x in a:
#     print(x)
# exit()


# print('--------------test generation of bcp out lines--------------------')
# bcpobj = sqlbcp(CONNECTION, database, DATAFOLDER, 'out', [], [], opt)
# dct = bcpobj.bcp()
# dict_results = {}
# for x in dct:
#     print(dct[x])
#
# print('--------------test generation of bcp in lines--------------------')
# database = 'AdventureWorks2012_BCP'
# bcpobj = sqlbcp(CONNECTION, database, DATAFOLDER + r'\AdventureWorks2012', 'in', [], [], opt)
# dct = bcpobj.bcp()
# dict_results = {}
# for x in dct:
#     print(dct[x])


# print('test one line bcp out')
# s = r'bcp AdventureWorks2012.Production.ProductReview out d:\temp\AdventureWorks2012.Production.ProductReview.dat -S"(local)\sql201
# d = runbcp(s)
# print(d)

# exit()

print('-----------------test all lines bcp out, no exec yet--------------------------------')
# CONNECTION = {}
# SQLSERVER = r'CCLTSTDTSDB6,3655'
# CONNECTION['servername'] = SQLSERVER
# CONNECTION['username'] = ''
# CONNECTION['password'] = ''
# database = 'ZZZ_Deleteme'
# print('Connection dict:', CONNECTION)
# DATAFOLDER = r'\\CCLTSTDTSDB6\SQLBACKUPS'
# opt = {'ext': '.bin', 'auto_db_folders': True}
# bcpobj = sqlbcp(CONNECTION, database, DATAFOLDER, 'out', [], [], opt)
# dct = bcpobj.bcp()
# for x in dct:
#     print(dct[x])
# LogBCP('out', CONNECTION, database, dct)
# exit()

print('-----------------test all lines bcp in, no exec yet--------------------------------')
CONNECTION = {}
SQLSERVER = r'CCLTSTDTSDB6,3655'
CONNECTION['servername'] = SQLSERVER
CONNECTION['username'] = ''
CONNECTION['password'] = ''
database = 'YYY_DELETEME'
print('Connection dict:', CONNECTION)
DATAFOLDER = r'\\CCLTSTDTSDB6\SQLBACKUPS\ZZZ_Deleteme'
opt = {'ext': '.bin', 'auto_db_folders': False}
bcpobj = sqlbcp(CONNECTION, database, DATAFOLDER, 'in', [], [], opt)
dct = bcpobj.bcp()
for x in dct:
    print(dct[x])
# print('deleting all rows in destination database (for testing re-runs)')
# res, lst = Delete_from_all_tables(CONNECTION, database)
# if res is True:
#     print('all records deleted')
# else:
#     print('deletion not successful')
#     for x in lst:
#         print(x)
# LogBCP('in', CONNECTION, database, dct)

# exit()


print('-------------doing threaded bcp in--------------------------')
items_to_process = len(dct)
# Using a default of 5 threads if pool not specified
if THREAD_POOL == 0:
    THREAD_POOL = int(items_to_process / 5)

print('Total items to process:', items_to_process)
print('Thread pool (concurrent processes): ', THREAD_POOL)
if NOEXECUTE_OPTION == 0:
    print('Execution option is yes')
else:
    print('No execution')

# Threading starts from here on: we have the dictionary with all the bcps
# lock to serialize console output
lock = threading.Lock()

# Create the queue and thread pool.
q = queue.Queue()
for i in range(THREAD_POOL):
    t = threading.Thread(target=worker)
    t.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
    t.start()

# stuff work items on the queue.
start1 = time.perf_counter()         # saving start time
for item in range(len(dct)):
    q.put(item)
    time.sleep(0.05)

q.join()                            # block until all tasks are done
# ----------------------------End-------------------------------------------


print('time:', time.perf_counter() - start1)
print('displaying results')
for x in DICT_RESULTS2:
    print(x)


