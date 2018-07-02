# version in HP PC at work
# last updated
# 7/27/2015 Changed LogSQL (more precision on saved date)
# 7/16/2015 Added ReadActionsFile and changed ReadActions
# 7/14/2015 replaced cfg files with single ACTIONS.DAT file, added ReadActions function
# 4/2/2015 tested with recent changes in SQLSMO
# 3/12/2015  fixed issue with empty lines in csv file, added log backups in actions
# 3/9/2015   added restore set of logs
# 3/4/2015   removed SyncLogins (it is already in included SQLSMO)
# 1/28/2015  added sql logging
# 1/28/2015  fixed again sitecoreadmin setup
# 1/26/2015  fixed sitecoreadmin setup
# 1/5/2015   tested with modified SQLSMO
# 12/30/2014 added backup
# 12/29/2014 added ok_to_restore call before restore
# 12/26/2014 added reset of Ys in source file ResetCSV(filename)
# 12/23/2014 completed set of actions, tested
# 12/15/2014 updated actionparsing
# 12/12/2014 - created from Threading_Restores.py

import sys
import threading
import queue
import csv
from SQLSMO import *


# =============== FUNCTIONS ===========================
def LogSQL(filename, CN, sql):
    """
    Appends to given log file the sql executed with this format:
    -----------------------------------
    --Server:   SERVERNAME
    --Database: DATABASE
    --Date:  Current date


    script line 1
    script line 2
    ...
    -----------------------------------
    """

    from datetime import datetime
    today = str(datetime.now())

    # today = str(datetime.date.today())
    f = open(filename, 'a')
    s = "\n\n-----------------------------------------------------\n\n"
    s += '--Server:   ' + CN['servername'] + "\n"
    s += '--Database: ' + CN['db'] + "\n"
    s += '--Date:     ' + today + "\n\n"
    s += sql
    s += "\n\n-----------------------------------------------------\n\n"
    f.write(s)
    f.close()

def ReadCSV(filename):
    """
    Returns array with entries marked as ENABLED=Y in source file
    """

    ary = []
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                if len(row) > 1 and row[-1].strip() == 'Y':
                    ary.append(row)
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
    return ary


def ResetCSV(filename):
    """
    Clears Enabled flag in source file to prevent accidental re-execution
    """

    s = ''
    f = open(filename)
    lst = f.readlines()
    for x in lst:
        if (x[-2:-1] == 'Y') | (x[-1] == 'Y'):
            m = x.replace(",Y", ",")
            s += m
        else:
            s += x
    f.close()
    f = open(filename, 'wt')
    f.write(s)
    f.close()


def ReadActionsFile(file):
    """
    Returns a list of actions from the file passed

    Sample file with two sets RESTORE SYSTEST and RESTORE AG PRIMARY:

    RESTORE SYSTEST
        RESTORE DATABASE RECOVERY
        SET SA DBOWNER
        SET SIMPLE MODE
        SHRINK LOG
        SYNC LOGINS
    RESTORE AG PRIMARY
        RESTORE DATABASE NORECOVERY
        RESTORE LOGS WITH RECOVERY
        SYNC LOGINS
    """

    list = []
    f = open(file)
    z = f.readlines()
    for x in z:
        m = x.rstrip()
        if (m != '') and (m[0] != '#'):
            list.append(x)
    return list

def ReadActions(filelines, set):

    """
    Returns a list of actions from the action list for the passed set
    A set is a collection of actions
    The action list is the parameter filelines, which is produced by the function ReadActionsFile

    Sample action list with two sets RESTORE SYSTEST and RESTORE AG PRIMARY:

    RESTORE SYSTEST
        RESTORE DATABASE RECOVERY
        SET SA DBOWNER
        SET SIMPLE MODE
        SHRINK LOG
        SYNC LOGINS
        RESTORE AG PRIMARY
        RESTORE DATABASE NORECOVERY
        RESTORE LOGS WITH RECOVERY
        SYNC LOGINS

    Set actions start with a tab or spaces (indented)
    Set names have no indentation (RESTORE SYSTEST, RESTORE AG PRIMARY)

    If the set name is duplicated below in the file the other sets are discarded
    Only the first one is used
    """

    list = []
    capture = False
    already_read = False
    for x in filelines:
        m = x.replace("\n", '')
        # print('m', m)
        if (m == set) and (already_read is False):
            capture = True
            already_read = True
        if (m[0] != chr(32)) and (m[0] != chr(9)) and (m != set):
            capture = False
        if ((m[0] == chr(32)) or (m[0] == chr(9))) and (capture is True):  # this means line is part of a set of tasks
            list.append(m.strip())
    return list


def ActionParsing(f):
    """
    Executes the actions from the source file, extracted from global ACTIONS_FILE_LIST
    """

    DESTSERVER = f[0]
    SOURCEDB = f[1]
    BACKUPFOLDER = f[2]
    DATAFOLDER = f[3]
    LOGFOLDER = f[4]
    DESTDB = f[5]
    ACTIONS = f[6]

    # get list of actions for the passed action tag
    action_list = ReadActions(ACTIONS_FILE_LIST, ACTIONS)

    CONNECTION = {}
    CONNECTION['servername'] = DESTSERVER
    CONNECTION['username'] = ''
    CONNECTION['password'] = ''
    CONNECTION['db'] = DESTDB

    msg = "\n"
    SQL = "\n"

    for m in action_list:
        m = m.strip()
        msg = msg + ' action:' + m + "\n"

        if m == 'SQL|BACKUP DATABASE FULL':
            DB_BACKUP = BACKUPFOLDER + '\\' + DESTDB + '_backup_' + DatedString() + BACKUP_MASK[-4:]    # .BAK
            smobackup = SQLSMO(CONNECTION, '', '', DB_BACKUP)   # database to backup is DESTDB
            smobackup.noexecute = NOEXECUTE_OPTION
            smobackup.BackupDatabase()
            SQL += smobackup.sqlbackup + "\n\n"

        elif m == 'SQL|BACKUP DATABASE LOG':
            DB_BACKUP = BACKUPFOLDER + '\\' + DESTDB + '_backup_' + DatedString() + LOG_MASK[-4:]       # .TRN
            smobackup = SQLSMO(CONNECTION, '', '', DB_BACKUP)   # database to backup is DESTDB
            smobackup.backup_options['backup_type'] = 'LOG'
            smobackup.noexecute = NOEXECUTE_OPTION
            smobackup.BackupDatabase()
            SQL += smobackup.sqlbackup + "\n\n"

        elif m == 'SQL|RESTORE DATABASE NORECOVERY':
            try:
                BKFILE = GetLatestBackup(BACKUPFOLDER, '\\' + SOURCEDB + BACKUP_MASK)[-1]
            except IndexError:
                print('No backup file!')
                break
            smo3 = SQLSMO(CONNECTION, DATAFOLDER, LOGFOLDER, BKFILE)
            smo3.noexecute = NOEXECUTE_OPTION
            smo3.restore_options['recovery'] = 'NORECOVERY'
            ok_to_restore = smo3.Ok_to_restore()
            if ok_to_restore:
                confirm_msg = 'Ok to restore'
            else:
                confirm_msg = 'NOT ok to restore'
                smo3.noexecute = 0
            msg = msg + confirm_msg + "\n"
            smo3.RestoreDatabase()
            SQL += smo3.sqlrestore + "\n\n"

        elif m == 'SQL|RESTORE LOG RECOVERY':
            s = BuildTlogSQL(DESTDB, SOURCEDB, BACKUPFOLDER, 'RECOVERY', BACKUP_MASK, LOG_MASK)
            if NOEXECUTE_OPTION == 0:
                try:
                    rows, fnames = SqlExecute(CONNECTION, s)
                except Exception as inst:
                    print('Error executing RESTORE LOGS RECOVERY ', inst)
                    break
            SQL += s + "\n\n"

        elif m == 'SQL|RESTORE LOG NORECOVERY':
            s = BuildTlogSQL(DESTDB, SOURCEDB, BACKUPFOLDER, 'NORECOVERY', BACKUP_MASK, LOG_MASK)
            if NOEXECUTE_OPTION == 0:
                try:
                    rows, fnames = SqlExecute(CONNECTION, s)
                except Exception as inst:
                    print('Error executing RESTORE LOGS NORECOVERY ', inst)
                    break
            SQL += s + "\n\n"

        elif m == 'SQL|RESTORE DATABASE RECOVERY':
            try:
                BKFILE = GetLatestBackup(BACKUPFOLDER, '\\' + SOURCEDB + BACKUP_MASK)[-1]
            except IndexError:
                print('No backup file!')
                break
            smo3 = SQLSMO(CONNECTION, DATAFOLDER, LOGFOLDER, BKFILE)
            smo3.noexecute = NOEXECUTE_OPTION
            ok_to_restore = smo3.Ok_to_restore()
            if ok_to_restore:
                confirm_msg = 'Ok to restore'
            else:
                confirm_msg = 'NOT ok to restore'
                smo3.noexecute = 0

            smo3.RestoreDatabase()
            msg += confirm_msg + "\n"
            SQL += smo3.sqlrestore + "\n\n"

        elif m == 'SQL|KILL CONNECTIONS':
            r = KillConnections(CONNECTION, DESTDB)
            msg += str(r) + "\n"

        # elif m == 'SET DBOWNER: sa':
        elif m == 'SQL|SET SA DBOWNER':
            s = 'USE [' + DESTDB + '] EXEC dbo.sp_changedbowner @loginame = N' + chr(39) + 'sa' + chr(39) + ', @map = false'
            try:
                rows, fnames = SqlExecute(CONNECTION, s)
            except Exception as inst:
                print('Error executing set dbowner sa: ', inst)
                break
            SQL += s + "\n\n"

        elif m == 'SQL|SYNC LOGINS':
            rows = SyncLogins(CONNECTION, DESTDB)
            for y in rows:
                msg += str(y) + "\n"

        elif m == 'SQL|SET SIMPLE MODE':
            s = 'USE [master] ALTER DATABASE [' + DESTDB + '] SET RECOVERY SIMPLE WITH NO_WAIT'
            try:
                rows, fnames = SqlExecute(CONNECTION, s)
            except Exception as inst:
                print('Error executing set simple mode ', inst)
                break
            SQL += s + "\n\n"

        elif m == 'SQL|SET FULL MODE':
            s = 'USE [master] ALTER DATABASE [' + DESTDB + '] SET RECOVERY FULL WITH NO_WAIT'
            try:
                rows, fnames = SqlExecute(CONNECTION, s)
            except Exception as inst:
                print('Error executing set full mode ', inst)
                break
            SQL += s + "\n\n"

        elif m == 'SQL|SHRINK LOG':
            s = '''
            declare @logfilename varchar(200)
            select @logfilename = name  from sysfiles where groupid = 0
            DBCC SHRINKFILE (@logfilename , 0, TRUNCATEONLY)
            '''
            s = 'USE [' + DESTDB + '] ' + s
            try:
                rows, fnames = SqlExecute(CONNECTION, s)
            except Exception as inst:
                print('Error executing shrink log ', inst)
                break
            SQL += s + "\n\n"

        elif m == 'SITECORE|SET SITECOREADMIN: DBO':
            s += 'USE [' + DESTDB + '] '
            s += ' if not exists (select name from sysusers where name = ' + chr(39) + 'sitecoreadmin' + chr(39) + ') create user [sitecoreadmin] for login [sitecoreadmin]; '
            s += ' ALTER USER [sitecoreadmin] WITH DEFAULT_SCHEMA=[dbo];'
            s += ' EXEC sp_addrolemember N' + chr(39) + 'db_owner' + chr(39) + ', N' + chr(39) + 'sitecoreadmin' + chr(39)
            try:
                SqlExecute(CONNECTION, s)
            except Exception as inst:
                print('Error executing set sitecoreadmin dbo ', inst)
            SQL += s + "\n\n"

    with lock:
        print(msg)
        print('Item processed: ', f)
        LogSQL(SQLFILE, CONNECTION, SQL)
    return f


#threading functions---------------------------------------------------
def do_work(item, f):
    """
    do lengthy work
    """

    start2 = time.perf_counter()         # saving start time
    line = ActionParsing(f)

    DICT_RESULTS = {}
    ThreadItem = threading.current_thread().name + '_' + str(item)
    DICT_RESULTS[ThreadItem] = {}
    DICT_RESULTS[ThreadItem]['line processed:'] = line

    time_elapsed = time.perf_counter() - start2
    DICT_RESULTS[ThreadItem]['ELAPSED TIME'] = time_elapsed
    DICT_RESULTS2.append(DICT_RESULTS)


def worker():
    """
    The worker thread pulls an item from the queue and processes it
    """

    while True:
        item = q.get()
        f = DBLIST2.pop()
        do_work(item, f)
        q.task_done()
# --------------end of threading functions--------------





# ===============End of functions=======================


# ============== Program Start==========================
if __name__ == '__main__':

    # ---------------Parameters-------------------------------------------------
    SOURCEFILE = ''
    paramlist = sys.argv
    print('Number of arguments:', len(paramlist), 'arguments.')
    print('Argument List:', str(paramlist))
    if len(paramlist) < 2:
        print('No source file provided, exiting')
        exit()
    else:
        print('Source file:', paramlist[1])
        SOURCEFILE = paramlist[1]
    #exit()
    # ---------------Parameters End----------------------------------------------

    # ---------------some global values------------------------------------------
    DICT_RESULTS2 = []                      # used to store execution messages, to be displayed at the end
    BACKUP_MASK = '_backup_201?*.bak'       # backup mask for full backup files in backup folder
    LOG_MASK = '_backup_201?*.TRN'          # mask for log backup files in backup folder
    NOEXECUTE_OPTION = 0                   # 1 = no execution, 0 = yes execution
    THREAD_POOL = 5                         # 0 means will process all entries in source file in its own thread
    SQLFILE = SOURCEFILE.replace('.CSV', '.SQL')
    ACTIONS_FILE = 'ACTIONS.DAT'
    ACTIONS_FILE_LIST = ReadActionsFile(ACTIONS_FILE)
    # ---------------some global values end---------------------------------------



    # csv file with list of Servers,DBs and desired actions
    DBLIST2 = ReadCSV(SOURCEFILE)
    items_to_process = len(DBLIST2)
    if THREAD_POOL == 0:
        THREAD_POOL = items_to_process

    print('Total items to process:', items_to_process)
    print('Thread pool (concurrent processes): ', THREAD_POOL)
    if NOEXECUTE_OPTION == 0:
        print('Execution option is yes')
    else:
        print('No execution')

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
    for item in range(len(DBLIST2)):
        # print('item:', item)
        q.put(item)

    q.join()       # block until all tasks are done

    print('time:', time.perf_counter() - start1)
    for x in DICT_RESULTS2:
        print(x)

    # clear enabled lines in source file after run (prevent accidental re-run)
    # ResetCSV(SOURCEFILE)