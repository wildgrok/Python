# sqlbcp.py
# Last modified:
# 4/24/2015 added option for user and password

# Note: copied SqlExecute locally
# from SQLSMO import SqlExecute
import subprocess
import os
import datetime
sqlbcp_outstream = []

# -------------functions------------------------------------------------
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
        constr = "sqlcmd -I -E -S" + conn['servername'] + "  /w 8192 -W " + ' -s' + conn['colseparator'] + '  '
    else:
        constr = "sqlcmd -I -U" + conn['username'] + " -P" + conn['password'] + ' -S' + conn['servername'] + '  /w 8192 -W  -s' + conn['colseparator'] + '  '

    # now we execute
    try:
        data = subprocess.Popen(constr + '-Q"' + sqlquery + '"', stdout=subprocess.PIPE).communicate()
    except Exception as inst:
        sqlbcp_outstream.append('Exception in SqlExecute:')
        sqlbcp_outstream.append(inst)
        # print('Exception in SqlExecute:', inst)
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


def GetTables(conn, database):
    """
    Returns list of tables in database
    """
    # query skips system tables like dbo.dtproperties
    s = 'set nocount on  use [' + database + '] '
    s = s + " select a.table_schema + '.' + a.table_name from INFORMATION_SCHEMA.TABLES a "
    s = s + " join sysobjects b on a.TABLE_NAME = b.name "
    s = s + " where a.table_type = 'base table' and LEFT(a.table_name, 1) <> '#' and b.category = 0 "

    rows, fnames = [], []
    outlist = []
    try:
        rows, fnames = SqlExecute(conn, s)
    except Exception as inst:
        sqlbcp_outstream.append('Error in GetTables:')
        sqlbcp_outstream.append(inst)
        #print('Error in GetTables: ', inst)
        return outlist
    for x in rows[1:]:
        outlist.append(x[0])
    return outlist

def GetFiles(datafolder, ext='.dat'):
    """
    Returns list of files in data folder for a given extension
    """

    import os
    filelist = []
    files = os.listdir(datafolder)
    for xfile in files:
            if os.path.isfile(datafolder + '\\' + xfile):
                if xfile[-4:] == ext:
                    filelist.append(xfile)
    return filelist


def Delete_from_all_tables(conn, db):
    """
    Deletes rows from all tables
    Returns True, empty list if deletion was effective
    Returns False, list of records not deleted if there were tables not deleted
    """

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
        sqlbcp_outstream.append('Error deleting data all tables:')
        sqlbcp_outstream.append(inst)
        #print('Error deleting data all tables: ', inst)
    # check if all rows were deleted
    cnt = 0
    badrows = []
    for x in rows:
        if x[0] != '0' and x[0] != '-' and x[0] != ' ' and len(x) > 1:
            cnt = cnt + 1
            badrows.append(x)
    if cnt > 0:
        return False, badrows
    else:
        return True, []



def runbcp(line):
    """
    Executes the passed bcp statement
    Starting copy...

    290 rows copied.
    Network packet size (bytes): 4096
    Clock Time (ms.) Total     : 593    Average : (489.04 rows per sec.)
    """

    data = []
    try:
        data = subprocess.Popen(line, stdout=subprocess.PIPE).communicate()
    except Exception as inst:
        sqlbcp_outstream.append('Exception in runbcp:')
        sqlbcp_outstream.append(inst)
        # print('Exception in runbcp:', inst)
        return inst
    return data[0].decode()

def LogBCP(in_out, CN, database, dct_bcplines, filename=''):
    """
    Creates bcp file with this format:
    -----------------------------------
    REM Server:   SERVERNAME
    REM Database: DATABASE
    REM Mode: in_out
    bcp line 1
    bcp line 2
    ...
    -----------------------------------
    If file name is not passed it will be created with this name
    SERVER_DATABASE_in.bat or SERVER_DATABASE_out.bat
    Any backslash or comma in server name will be replaced by underscore in the file name
    """
    if filename == '':
        f1 = CN['servername'] + '_' + database + '_' + in_out + '.bat'
        f2 = f1.replace('\\', '_')
        f3 = f2.replace(',', '_')
    today = str(datetime.date.today())
    f = open(f3, 'w')
    s = "\n\n"
    s += 'REM Server:   ' + CN['servername'] + "\n"
    s += 'REM Database: ' + database + "\n"
    s += 'REM Mode: ' + in_out + "\n"
    s += 'REM Date:     ' + today + "\n\n"
    for x in dct_bcplines:
        s = s + dct_bcplines[x] + "\n"
    s += "\n\n"
    f.write(s)
    f.close()

# --------------end of functions------------------------

class sqlbcp:
    """
    usage: bcp {dbtable | query} {in | out | queryout | format} datafile
      [-m maxerrors]            [-f formatfile]          [-e errfile]
      [-F firstrow]             [-L lastrow]             [-b batchsize]
      [-n native type]          [-c character type]      [-w wide character type]
      [-N keep non-text native] [-V file format version] [-q quoted identifier]
      [-C code page specifier]  [-t field terminator]    [-r row terminator]
      [-i inputfile]            [-o outfile]             [-a packetsize]
      [-S server name]          [-U username]            [-P password]
      [-T trusted connection]   [-v version]             [-R regional enable]
      [-k keep null values]     [-E keep identity values]
      [-h "load hints"]         [-x generate xml format file]
      [-d database name]        [-K application intent]
    """

    def __init__(self, conn, database, datafolder, action, tablelist=[], filelist=[], options={}):
        self.conn = conn
        self.sqlserver = conn['servername']
        self.username = conn['username']
        self.password = conn['password']
        self.database = database
        self.datafolder = datafolder
        self.tablelist = tablelist
        self.filelist = filelist
        self.action = action
        if options == {}:
            options['ext'] = '.dat'
            options['auto_db_folders'] = False
        self.extension = options['ext']
        self.auto_db_folders = options['auto_db_folders']
        if self.auto_db_folders is True and self.action == 'out':
            try:
                os.mkdir(datafolder + "\\" + database)
            except FileExistsError as inst:
                sqlbcp_outstream.append('DB folder already exists')
                # sqlbcp_outstream.append(inst)
                # print('DB folder already exists')
            self.datafolder = datafolder + "\\" + database


        if len(tablelist) == 0:
            self.tablelist = GetTables(self.conn, self.database)
        if len(filelist) == 0 and action == 'in':
            self.filelist = GetFiles(datafolder, self.extension)


    def bcp(self):
        """
        Fills a dictionary with bcp lines
        If tablelist=[], filelist=[] they are created from database and work folder
        Fixed options are -E (keep identity and -n (native mode)
        """

        bcpdict = {}
        tablecount = len(self.tablelist)
        filecount = len(self.filelist)

        if self.username == '':
            scon = ' -S"' + self.sqlserver + '" -T -E -n ' + ' -d"' + self.database + '" -q'
        else:
            scon = ' -S"' + self.sqlserver + '"  -U' + self.username + ' -P' + self.password + ' -E -n ' + ' -d"' + self.database + '" -q'
        if self.action == 'out':
            for tablename in self.tablelist:
                bcpdict[tablename] = 'bcp ' + tablename + ' ' + self.action + ' ' + self.datafolder + '\\' + tablename + self.extension + scon
        if self.action == 'in':
            if filecount == 0:
                sqlbcp_outstream.append('Need to pass file list')
                # print('Need to pass file list')
                return bcpdict
            else:
                if tablecount > filecount:
                    print('***Missing files for tables***')
                    for table in self.tablelist:
                        for file in self.filelist:
                            if file[:-4] == table:
                                bcpdict[tablename] = 'bcp ' + table + ' ' + self.action + ' ' + self.datafolder + '\\' + table + self.extension + scon

                if tablecount <= filecount:
                    for file in self.filelist:
                        for table in self.tablelist:
                            if file[:-4] == table:
                                bcpdict[table] = 'bcp ' + table + ' ' + self.action + ' ' + self.datafolder + '\\' + table + self.extension + scon

        # print('tablecount', tablecount, 'filecount', filecount)
        sqlbcp_outstream.append('tablecount')  #, tablecount, 'filecount', filecount)
        sqlbcp_outstream.append(tablecount)
        sqlbcp_outstream.append('filecount')
        sqlbcp_outstream.append(filecount)
        return bcpdict


