# __author__ = 'JorgeBe'
# print("hello")

# import win32com, win32com.client
# import datetime, glob, os
import subprocess
from pprint import pprint


# def add_acct(location,account):
# ad_obj=win32com.client.GetObject(location)
#
#   ad_user=ad_obj.Create('user','cn='+user['login'])
#   ad_user.Put('sAMAccountName',user['login'])
#   ad_user.Put('userPrincipalName',user['login']+'@email.address.com')
#   ad_user.Put('DisplayName',user['last']+' '+user['first']) #fullname
#   ad_user.Put('givenName',user['first'])
#   ad_user.Put('sn',user['last'])
#   ad_user.Put('description','regular account')
#   ad_user.Put('physicalDeliveryOfficeName','office 1')
#   #ad_user.Extensionattribute10='your own attribute'
#   ad_user.Put('HomeDirectory',r'\\server1\ '[:-1]+user['login'])
#   ad_user.Put('HomeDrive','H:')
#   ad_user.SetInfo();ad_user.GetInfo()
#   ad_user.LoginScript='login.bat'
#   ad_user.AccountDisabled=0
#   ad_user.setpassword('the password')
#   ad_user.Put('pwdLastSet',0) #-- force reset of password
#   ad_user.SetInfo()


# location='LDAP://OU=org1,DC=carnival,DC=com'
#user={'first':'fred','last':'smith','login':'fred123'}
#add_acct(location,user)
# location='LDAP://OU=.,DC=carnival,DC=com'
# ad_obj=win32com.client.GetObject()

# ad_obj=win32com.client.GetObject(location)
# for x in ad_obj:
#     {
#         print(x)
#     }

#---------------------------------------------------------------------------
def GetLDAPInfo(netuser):
    """
    Returns LDAP info for netuser
    Sample call:
    lst = GetLDAPInfo('carnival\\jorgebe')
    print(lst)
    ('LDAP://CN=Besada\\, Jorge L. (CCL),OU=Information Systems,OU=Business Units,OU=Carnival Headquarters,DC=carnival,DC=com', 'JBesada@carnival.com')
    """


    name_resolver = win32com.client.Dispatch(dispatch='NameTranslate')
    name_resolver.Set(3, netuser)
    ldap_query = 'LDAP://{}'.format(name_resolver.Get(1))
    ldap = win32com.client.GetObject(ldap_query)
    return ldap_query, ldap.Get('mail')


#---------------------------------------------------------------------------


# with open(fname, 'r', encoding="ascii", errors="surrogateescape") as f:
#     data = f.read()
#
# # make changes to the string 'data'
#
# with open(fname + '.new', 'w',
#            encoding="ascii", errors="surrogateescape") as f:
#     f.write(data)







#---------------------------------------------------------------------------
def ScrubFile(filein, fileout, strtoremove):
    """
    Cleans input file line by line
    """
    lines = 0
    #outfile = open(fileout, 'wt',encoding="ascii", errors="surrogateescape", newline='\n')
    # outfile = open(fileout, 'wt', encoding="utf-16")
    outfile = open(fileout, 'wt', encoding="ascii")
    infile = open(filein, 'rt', encoding="ascii", errors="surrogateescape", newline='\n')
    x = infile.read()
    y = x.replace(strtoremove,'')
    try:
        outfile.write(y)
    except UnicodeEncodeError:
        pass
    #outfile.write('')
    # for x in infile:
    #     outfile.write(x.replace(strtoremove,''))
    #     lines = lines + 1

    outfile.close()
    return lines

#---------------------------------------------------------------------------
# now1 = datetime.datetime.now()
# print(now1)
# lines = ScrubFile(r'd:\temp\person_sbl_push_group_01.csv', r'd:\temp\person_sbl_push_group.out' , "'")
# now2 = datetime.datetime.now()
# print(now2)
# print(now2-now1)


#------------------------------------------------------------------------
def StandarizeFileCommas():
    """
    Standardizes the number of commas per line prior to being read by
    programs such as BCP and required for compliance with RFC4180 for CSV files
    initialize the variables, change FileNames as appropriate
    """
    InFileName = r'C:\test\testimport.csv'
    OutFileName = r'C:\test\testimport2.csv'
    NumCommas = 0

    File = open(InFileName)

    for line in File:
        if line.count(',') > NumCommas:
            NumCommas = line.count(',')

    #return to the start of the file
    File.seek(0)

    OutFile = open(OutFileName, 'w')
    for line in File:
        OutFile.write(line.rstrip() + ',' * (NumCommas - line.count(',')) + '\n')

    OutFile.close()
    File.close()
#------------------------------------------------------------------------





#--------------------------------------------------------------------
def GetLatestBackup(dirpath, filter='\*.*'):
    """
    Returns folder contents sorted by modified date
    Sample use:
    backupfolder = r'\\SERVERNAME\SQLBackups1\SQLBackupUser'
    This brings all files
    lst = GetLatestBackup(backupfolder)
    Here we bring a subset using filter string
    filter = '\DATABASE_*.bak'
    lst = GetLatestBackup(backupfolder, filter)
    """
    a = [s for s in glob.glob(dirpath + filter) if os.path.isfile(os.path.join(dirpath, s))]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return a

#--------------------------------------------------------------------
# backupfolder = r'\\CCLPRDECODB1\SQLBackups1\SQLBackupUser'
# lst = GetLatestBackup(backupfolder)
# print(lst)
# Show the percentage free space for each fixed disk
# import wmi
# c = wmi.WMI ()
# for disk in c.Win32_LogicalDisk (DriveType=3):
#     #print (disk.Caption, "%0.2f%% free" % (100.0 * long (disk.FreeSpace) / long (disk.Size)))
#     #print (disk.Caption, "%0.2f%% free" % (100.0 * disk.FreeSpace /  disk.Size))
#     print (disk.Caption, disk.FreeSpace, disk.Size)






#------------------------------------------------------------
#example list service packs
#https://www.simple-talk.com/sql/database-administration/comparing-python-and-powershell-dba-scripting-/

# import string,sys,win32com.client
# from win32com.client import DispatchBaseClass
# ListOfServers='c:\\MyDir\\AFewServers.txt'
# txtfile = open('C:\\MyDir\\DSTPatched.txt','w')
# for line in open(ListOfServers,'r').readlines():
#  servers = string.split(string.strip(line),'\n')
#  svr=servers[0]
#  print svr
#  objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
#  objSWbemServices = objWMIService.ConnectServer(svr,"root\cimv2")
#  colItems = objSWbemServices.ExecQuery("Select * from
# Win32_QuickFixEngineering Where ServicePackInEffect = 'KB928388'")
#  for objItem  in colItems:
#   txtfile.write ('CS Name: ' + str(objItem.CSName) + '\n')
#   txtfile.write ('Service Pack In Effect: ' +
# str(objItem.ServicePackInEffect) + '\n')
#   txtfile.write ('\n')
# txtfile.close
#------------------------------------------------------------


#http://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python
def getfiles(dirpath, filter='\*.*'):
    """
    Returns folder contents sorted by modified date
    """

    a = [s for s in glob.glob(dirpath + filter) if os.path.isfile(os.path.join(dirpath, s))]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return a

# filter = '\CCL_GUEST_LOYALTY_*.bak'
# backupfolder = r'\\CCLPRDECODB1\SQLBackups1\SQLBackupUser'
# lst = getfiles(backupfolder)
# print(lst)
# lst = getfiles(backupfolder, filter)
# print(lst)

def ReadCSV(filename):
    import csv, sys
    ary = []
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
               # print(row)
                ary.append(row)
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
        return ary


# a = ReadCSV(r'\\ccldevsql1\RESTOREDBS\DBLIST.csv')
# print(a[0][-1])
# a = ReadCSV(r'temperatures.csv')
# print(a)

# Person = namedtuple('Patient', ['name', 'date', 'time', 'temp'])

'''
EmployeeRecord = namedtuple('EmployeeRecord', 'name, age, title, department, paygrade')

import csv
for emp in map(EmployeeRecord._make, csv.reader(open("employees.csv", "rb"))):
    print(emp.name, emp.title)

'''


def ReadPatientCSV(filename):
    """
    Usage:
    k = ReadPatientCSV(r'temperatures.csv')
    print('------')
    pprint(k)
    """
    from collections import namedtuple
    import csv, sys

    persons = []
    Person = namedtuple('Patient', ['name', 'date', 'time', 'temp'])
    try:
        for emp in map(Person._make, csv.reader(open(filename, "r"))):
            # print(emp, emp.name)
            persons.append(emp)
    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(filename, csv.reader.line_num, e))
    return persons

# k = ReadPatientCSV(r'temperatures.csv')
# print('------')
# pprint(k)

def fix_com_exception(e):
    e.hresult = fix_com_hresult(e.hresult)
    e.args = [e.hresult] + list(e.args[1:])
    return e

def fix_com_hresult(hr):
    import struct
    return struct.unpack("L", struct.pack("l", hr))[0]
#which can then be used how you expect:

# DISP_E_EXCEPTION = 0x80020009
# try:
#     #failing call
# except pywintypes.com_error as e:
#     print repr(e)
#     #pywintypes.com_error: (-2147352567, 'Exception occurred.', (0, None, None, None, 0, -2146788248), None)
#     fix_com_exception(e)
#     print repr(e)
#     #pywintypes.com_error: (2147614729L, 'Exception occurred.', (0, None, None, None, 0, -2146788248), None)
#     if e.hresult == DISP_E_EXCEPTION:
#         print "Got expected failure"
#     else:
#         raise

def SqlConnect(servername = '',username = '',password = '', defdb = 'master'):
    import win32com.client
    connection = win32com.client.Dispatch(r'ADODB.Connection')
    # Connection State Constants
    #
    adStateClosed	    = 0
    adStateOpen	        = 1
    adStateConnecting	= 2
    adStateExecuting	= 4
    adStateFetching	    = 8

    if username == '':
            #self.constr = "Provider=SQLNCLI11;Server=" + self.servername + ";Integrated Security=SSPI; database=" + self.defdb
        constr = "Provider=SQLOLEDB.1;Data Source=" + servername + ";Trusted_Connection=yes; database=" + defdb
    else:
        constr = "Provider=SQLOLEDB.1;Data Source=" + servername + ";uid=" + username + ";pwd=" + password + "; database=" + defdb
    try:
        connection.Open(constr)
        if connection.State == adStateOpen:
            return connection
    except Exception as inst:
        print('Exception in SqlConnect:', inst)
        return -1



def SqlExecute_RS(conn, sql):
    try:
        recordset = conn.execute(sql)
    except Exception as inst:
        print('Exception in SqlExecute:', inst)
        return -1

    records = []
    fieldnames = []
    for x in range(recordset.Fields.Count):
        fieldnames.append(recordset.Fields.Item(x).Name)
        #Need the try for not select type of sql, like updates, inserts
    values_list = []
    try:
        data = recordset.GetRows()
        rowcount = len(data[0])
        for y in range(0, rowcount):
            for x in data:
                values_list.append(x[y])
            records.append(tuple(values_list))
            values_list = []
        records = tuple(records)
    except UnboundLocalError:
        pass
    except:
        pass

    return records, fieldnames



def DeleteOlderFiles(workfolder, days):

    import os, time
    now = time.time()
    cutoff = now - (days * 86400)

    files = os.listdir(workfolder)
    for xfile in files:
            if os.path.isfile(workfolder + '\\' + xfile):
                t = os.stat(workfolder + '\\' + xfile )
                c = t.st_ctime

                # delete file if older than a week
                if c < cutoff:
                    print('deleting ' + xfile)
                    os.remove(workfolder + '\\' + xfile )


def ResetCSV(filename):

    """
    Clears Enabled flag in source file to prevent accidental re-execution
    """

    s = ''
    m = ''
    f = open(filename)
    lst = f.readlines()
    print('lst', lst)
    for x in lst:
        #print(x, x[-1])
        if (x[-2:-1] == 'Y') | (x[-1] == 'Y'):
            print('updating line', x)
            m = x.replace(",Y", ",")
            s = s + m
        else:
            s = s + x
    f.close()
    print('s:', s)
    f = open(filename, 'wt')
    f.write(s)
    f.close()


def file_name_dayofweek():
    from datetime import datetime

    now = datetime.now()
    day_name = now.strftime("%A")
    file_name = "%s.sql" % day_name.lower()
    #logging.debug("Setting backup name for day name %s as %s" % (day_name, file_name))
    return file_name

#ActionTags_backup_2014_12_28_140001_5613417
#                  2014-12-30 13:39:39.848057
def DatedString():
    """
    Returns dated string with this format
    2014_12_30_135857_4581860
    """
    from datetime import datetime
    now = str(datetime.now())
    now = now.replace('-', '_')
    now = now.replace(' ', '_')
    now = now.replace(':', '')
    now = now.replace('.', '_') + '0'
    return now

def SqlExecute(conn, sqlquery=''):

    """
    Executes sqlquery and returns lists with column names and data
    The connection info is passed as a dictionary with these required keys:
    servername, username,password
    If username is empty will use integrated security
    These keys are optional: defdb, colseparator
    """

    if 'colseparator' not in conn.keys():
        conn['colseparator'] = chr(1)
    if conn['username'] == '':
        constr = "sqlcmd -E -S" + conn['servername'] + "  /w 8192 -W " + ' -s' + conn['colseparator'] + '  '
    else:
        constr = "sqlcmd -U" + conn['username'] + " -P" + conn['password'] + ' -S' + conn['servername'] + '  /w 8192 -W  -s' + conn['colseparator'] + '  '

    # now we execute
    try:
        data = subprocess.Popen(constr + '-Q"' + sqlquery + '"', stdout=subprocess.PIPE).communicate()
    except Exception as inst:
        print('Exception in SqlExecute:', inst)
        return -1

    records = []
    lst = data[0].splitlines()
    # lst[0] column names;  lst[1] dashed lines, (skip); lst[2:] data
    # now we decode
    for x in lst:
        try:
            #try default utf-8 decoding
            line = x.decode()
        except UnicodeDecodeError:
            #in case of weird characters this one works most of the time
            line = x.decode('ISO-8859-1')
        lst2 = line.split(conn['colseparator'])
        records.append(lst2)
    fieldnames = records[0]
    data = records[2:]

    return data, fieldnames


def KillConnectionsOLD(conn, db):
    """
    Kills connections in database if database exists
    """

    s = 'SET NOCOUNT ON use master declare @db int select @db  = count(*) from master.dbo.sysdatabases where name = ' + chr(39) + \
    db + chr(39) + ' if (@db > 0) ALTER DATABASE [' + \
    db + '] SET  SINGLE_USER WITH ROLLBACK IMMEDIATE ALTER DATABASE [' + \
    db + '] SET  MULTI_USER WITH ROLLBACK IMMEDIATE'

    try:
        rows, fnames = SqlExecute(conn, s)
    except Exception as inst:
            print('Error killing connections: ', inst)
    return rows


def BuildTlogSQL(dbname, bkfolder, recovery = 'NORECOVERY'):
    """
    - check for log backups
    DECLARE backupFiles CURSOR FOR
    SELECT backupFile
    FROM @fileList
    WHERE backupFile LIKE '%.TRN'
    AND backupFile LIKE @dbName + '%'
    AND backupFile > @lastFullBackup
    OPEN backupFiles
    -- Loop through all the files for the database
    FETCH NEXT FROM backupFiles INTO @backupFile
    WHILE @@FETCH_STATUS = 0
    BEGIN
       SET @cmd = 'RESTORE LOG ' + @dbName + ' FROM DISK = '''
           + @backupPath + @backupFile + ''' WITH NORECOVERY'
       PRINT @cmd
       FETCH NEXT FROM backupFiles INTO @backupFile
    END
    CLOSE backupFiles
    DEALLOCATE backupFiles
    -- 6 - put database in a useable state
    SET @cmd = 'RESTORE DATABASE ' + @dbName + ' WITH RECOVERY'
    PRINT @cmd
    """

    BKFILE = '____.BAK'
    BACKUP_MASK = '_backup_20*.BAK'
    try:
        BKFILE = GetLatestBackup(bkfolder, '\\' + dbname + BACKUP_MASK)[-1]
    except IndexError:
        print('No full backup file')
    # print('BKFILE', BKFILE)
    s = ''
    filter = '\\' + dbname + '_backup_20*.TRN'
    filelist = GetLatestBackup(bkfolder, filter )

    for x in filelist:
        # test print
        # print(x)
        if x[:-4] > BKFILE[:-4]:
            s = s + 'RESTORE LOG ' + dbname + ' FROM DISK = ' + chr(39)  +  x + chr(39)  + \
                ' WITH NORECOVERY' + chr(13) + chr(10) + 'GO ' +  chr(13) + chr(10)
    if x[:-4] > BKFILE[:-4]:
        if recovery == 'RECOVERY':
            s = s + 'RESTORE DATABASE ' + dbname + ' WITH RECOVERY' + chr(13) + chr(10) + 'GO ' +  chr(13) + chr(10)
    return s


def KillConnections(conn, db):
    """
    Kills connections in database if database exists
    """

    s = 'SET NOCOUNT ON DECLARE @kill varchar(8000) = ' + chr(39) + chr(39) + ';'
    s = s + ' SELECT @kill = @kill + ' + chr(39) + 'kill ' + chr(39) + '  + CONVERT(varchar(5), spid) + ' + chr(39) + ';' + chr(39)
    s = s + ' FROM master..sysprocesses WHERE dbid = db_id(' + chr(39) + db + chr(39) + ')'
    s = s +  ' select @kill; EXEC(@kill);'

    rows = []
    try:
        rows, fnames = SqlExecute(conn, s)
    except Exception as inst:
            print('Error killing connections: ', inst)
    return rows

# import subprocess
# import sys
#
# #on windows
# #Get the fixed drives
# #wmic logicaldisk get name,description
# if 'win' in sys.platform:
#     drivelist = subprocess.Popen('wmic logicaldisk get name,description', shell=True, stdout=subprocess.PIPE)
#     drivelisto, err = drivelist.communicate()
#     driveLines = drivelisto.split('\n')
# elif 'linux' in sys.platform:
#      listdrives=subprocess.Popen('mount', shell=True, stdout=subprocess.PIPE)
#      listdrivesout, err=listdrives.communicate()
#      for idx,drive in enumerate(filter(None,listdrivesout)):
#          listdrivesout[idx]=drive.split()[2]
# # guess how it should be on mac os, similar to linux , the mount command should
# # work, but I can't verify it...
# elif 'macosx' ...
#      do the rest....






def FindFolder(serverlist, foldername=''):
    import subprocess
    import sys
    s = ''
    m = ''
    f = open(serverlist)
    lst = f.readlines()
    # print('lst', lst)
    cnt = 0
    for x in lst:
        # get server name from sql name or server with port added
        a = x.split('\\')
        b = a[0].replace(',3655', '').strip()
        if len(b) == 0:
            break
        print(b)
        # drivelist = subprocess.Popen('wmic logicaldisk get name,description', shell=True, stdout=subprocess.PIPE)
        # drivelisto, err = drivelist.communicate()
        # print(drivelisto)
        # # driveLines = drivelisto.split('\n')
        cnt += 1
        # if cnt > 4:
        #     return
    f.close()


def CheckDBFolders(conn, datafolder, logfolder):
    """
    Verifies the existance of provided data and log folders
    Sample output of query
    [['0', '1', '1'],
    ['File Exists', 'File is a Directory', 'Parent Directory Exists'],
    ['-----------', '-------------------', '-----------------------'],
    ['0', '1', '1']]
    """

    s = 'set nocount on;exec [sys].[xp_fileexist] ' + chr(39) + datafolder + chr(39) + ';exec [sys].[xp_fileexist] ' + chr(39) + logfolder + chr(39)
    rows = []; fnames = []
    try:
        rows, fnames = SqlExecute(conn, s)
    except Exception as inst:
        print('Error on CheckDBFolders: ', inst)

    dataflag = rows[0][1]
    logflag = rows[3][1]
    msg = ''
    if dataflag == '1' and logflag == '1':
        return True
    else:
        if logflag != '1':
            msg = 'Bad log folder ' + logfolder + "\n"
        if dataflag != '1':
            msg = msg + 'Bad data folder ' + datafolder + "\n"
        print(msg)
        return False


def ReadWebTable(htmldoc):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(htmldoc)
    return soup.findAll('table')


def makelist(table):
    result = []
    #allrows = table.findAll('tr')
    allrows = table.split('tr')
    for row in allrows:
        result.append([])
        #allcols = row.findAll('td')
        # allcols = row.split('td')
        # for col in allcols:
        #     # thestrings = [unicode(s) for s in col.findAll(text=True)]
        #     thestrings = [s for s in col.find(text=True)]
        #     thetext = ''.join(thestrings)
        #     result[-1].append(thetext)
    return result


def Delete_from_all_tables(conn, db):
    pass

    s = '''
    EXEC sp_MSForEachTable 'ALTER TABLE ? NOCHECK CONSTRAINT ALL'
    EXEC sp_MSForEachTable 'ALTER TABLE ? DISABLE TRIGGER ALL'
    EXEC sp_MSForEachTable 'SET QUOTED_IDENTIFIER ON; DELETE FROM ?'
    EXEC sp_MSForEachTable 'ALTER TABLE ? CHECK CONSTRAINT ALL'
    EXEC sp_MSForEachTable 'ALTER TABLE ? ENABLE TRIGGER ALL'
    EXEC sp_MSFOREACHTABLE 'select count(*), ''?'' FROM ?'
    '''

     # sqlcmd needs single line sql commands for the -Q option
    s = s.replace("\n", ' ')

    s2 = 'SET NOCOUNT ON USE [' + db + '] ' + s
    rows, fnames = [], []
    try:
        rows, fnames = SqlExecute(conn, s2)
    except Exception as inst:
        print('Error deleting data all tables: ', inst)

    # lst = []
    # rows2 = []
    # for x in rows:
    #     if x[0] != '0' and x[0] != '-' and x[0] != ' ' and len(x) > 1:
    #         lst.append(x)
    #         s3 = 'delete from ' + x[1]
    #         s4 = 'SET NOCOUNT ON USE [' + db + '] ' + s3
    #         rows2, fnames2 = [], []
    #         try:
    #             rows2, fnames2 = SqlExecute(conn, s4)
    #         except Exception as inst:
    #             print('Error deleting from ' + x[1], inst)
    return rows

def ReadActions_ORIGINAL(file, set):

    """
    Returns a list of actions from the file for the passed set
    A set is a collection of actions
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

    Set actions start with a tab or spaces (indented)
    Set names have no indentation (RESTORE SYSTEST, RESTORE AG PRIMARY)

    If the set name is duplicated below in the file the other sets are discarded
    Only the first one is used
    """

    list = []
    capture = False
    already_read = False
    f = open(file)
    z = f.readlines()
    # print('z', z)
    for x in z:
        m = x.rstrip()
        if (m == '') or (m[0] == '#'):
            # skip this line
            pass
        else:
            if (m == set) and (already_read is False):
                capture = True
                already_read = True
            if (m[0] != chr(32)) and (m[0] != chr(9)) and (m != set):
                capture = False
            if ((m[0] == chr(32)) or (m[0] == chr(9))) and (capture is True):  # this means line is part of a set of tasks
                list.append(m.strip())
    return list

# End of ReadActions

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

def GetPageWithProxy(url):
    import urllib.request as req
    proxy = req.ProxyHandler({'http': r'http://jorgebe:Justzoot!@proxy.carnival.com:8080'})
    auth = req.HTTPBasicAuthHandler()
    opener = req.build_opener(proxy, auth, req.HTTPHandler)
    req.install_opener(opener)
    conn = req.urlopen(url)
    return_str = conn.read()
    print(return_str)


def search(search_string):

    """
    http://stackoverflow.com/questions/26642655/how-can-i-get-google-search-results-with-python-3
    """
    import urllib.request
    import json



    query = urllib.parse.urlencode({'q': search_string})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    search_response = urllib.request.urlopen(url)
    search_results = search_response.read().decode("utf8")
    results = json.loads(search_results)
    data = results['responseData']
    print('Total results: %s' % data['cursor']['estimatedResultCount'])
    hits = data['results']
    print('Top %d hits:' % len(hits))
    for h in hits: print(' ', h['url'])
    print('For more results, see %s' % data['cursor']['moreResultsUrl'])
    return hits




# =============================================================================================

if __name__ == '__main__':
    pass

    # dct = ReadActionsFile(r'D:\JetBrains\PyCharm Community Edition 3.4.1\dblib3\ACTIONS.DAT')
    # print(dct)

    # lst = ReadActions(r'D:\JetBrains\PyCharm Community Edition 3.4.1\dblib3\ACTIONS.DAT', 'RESTORE SYSTEST')
    # print(lst)
    #
    # dct = ReadActionsFile(r'D:\JetBrains\PyCharm Community Edition 3.4.1\dblib3\ACTIONS.DAT')
    # print(dct)
    #
    # lst = ReadActions(dct, 'RESTORE SYSTEST')
    # print(lst)


    # conn = {}
    # conn['servername'] = '(local)\sql2014'
    # conn['username'] = ''
    # conn['password'] = ''
    # db = 'AdventureWorks2012_BCP'
    # r = Delete_from_all_tables(conn, db)
    # for x in r:
    #     print(x)

    # htmldoc = r'D:\JetBrains\PyCharm Community Edition 3.4.1\Toolkit\htmldoc.html'
    # r = ReadWebTable(htmldoc)
    # for x in r:
    #     print(x)
    # htmldoc = r'D:\JetBrains\PyCharm Community Edition 3.4.1\Toolkit\htmldoc.html'
    # f = open(htmldoc)
    # s = f.read()
    # print(s)
    # lst = makelist(s)
    # for x in lst:
    #     print(x)

    # conn = {}
    # conn['servername'] = '(local)\sql2014'
    # conn['username'] = ''
    # conn['password'] = ''
    # datafolder = r'D:\SQL2014\DATABASES'
    # logfolder = r'D:\SQL2014\DATABASES1'
    # r = CheckDBFolders(conn, datafolder, logfolder)
    # print(r)

    # FindFolder(r'D:\JetBrains\PyCharm Community Edition 3.4.1\Toolkit\serverlist.txt')
    # s = BuildTlogSQL('CCL_CS_INFO', r'\\CCLPRDDTSDB1F\tempbackups', 'RECOVERY')
    # print(s)


    #print(DatedString())
    #print(backup_name_dayofweek())
    #DeleteOlderFiles(r'\\Ccltstecosqldb1\sqlbackups', 0)
    #ResetCSV(r'D:\JetBrains\PyCharm Community Edition 3.4.1\dblib3\DBLIST_ACTIONS.CSV')
    #backupfolder = r'\\CCLPRDECODB1\SQLBackups1\SQLBackupUser'
    #lst = GetLatestBackup(backupfolder, '\CCL_Guest_Loyalty_*_2014_12_??_*.*')
    #print(lst[-1])

    #CCL_Guest_Loyalty_Log Backup_Subplan_1_20141231110002
    #CCL_Guest_Loyalty_backup_2014_12_30_120000_9528347
    # print('testing select query')
    # conn = {}
    # conn['servername'] = '(local)\sql2014'
    # conn['username'] = ''
    # conn['password'] = ''
    #
    # # sqlexecute w/o return values
    # SqlExecute(conn, 'set nocount on exec sp_helpdb')
    #
    # #testing select query
    # rows, fnames = SqlExecute(conn, 'set nocount on select top 10  * from AdventureWorks2012.Person.Person')
    # print(fnames)
    # for x in rows:
    #     print(x)

    # data , fnames = SqlExecute(conn, 'set nocount on select top 10  * from AdventureWorks2012.Person.Person')
    #
    # print(fnames)
    # print(data)
    #
    # r = KillConnections(conn, 'AdventureWorks2012')
    # for x in r:
    #     print(x)
    #
    # exit()

    # GetPageWithProxy('http://www.google.com') #, 'jorgebe', 'xxxxxxxxx', 'proxy.carnival.com:8080')
    search_string = 'trump'
    res = search(search_string)
    for x in res:
        print(x)