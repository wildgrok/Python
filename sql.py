import win32com.client
import os

sqlsynclogins = '''
DECLARE @UserName nvarchar(255)
DECLARE @SQLCmd nvarchar(511)
DECLARE orphanuser_cur cursor for
SELECT UserName = name
FROM sysusers
WHERE issqluser = 1 and (sid is not null and sid <> 0x0)
                and suser_sname(sid) is null
ORDER BY name

OPEN orphanuser_cur
FETCH NEXT FROM orphanuser_cur INTO @UserName

WHILE (@@fetch_status = 0)
BEGIN
select @UserName + ' user name being resynced'
set @SQLCmd = 'ALTER USER '+@UserName+' WITH LOGIN = '+@UserName
EXEC (@SQLCmd)
FETCH NEXT FROM orphanuser_cur INTO @UserName
END
CLOSE orphanuser_cur
DEALLOCATE orphanuser_cur
'''



def SqlConnect(servername = '',username = '',password = '', defdb = 'master'):
    connection = win32com.client.Dispatch(r'ADODB.Connection')
    # Connection State Constants
    adStateClosed	    = 0
    adStateOpen	        = 1
    adStateConnecting	= 2
    adStateExecuting	= 4
    adStateFetching	    = 8

    if username == '':
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


def SqlExecute(conn, sql):
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


def SqlExecute2(servername = '',username = '',password = '', defdb = 'master', sqlquery=''):
    connection = win32com.client.Dispatch(r'ADODB.Connection')
    # Connection State Constants
    #
    adStateClosed	    = 0
    adStateOpen	        = 1
    adStateConnecting	= 2
    adStateExecuting	= 4
    adStateFetching	    = 8

    if username == '':
        constr = "Provider=SQLOLEDB.1;Data Source=" + servername + ";Trusted_Connection=yes; database=" + defdb
    else:
        constr = "Provider=SQLOLEDB.1;Data Source=" + servername + ";uid=" + username + ";pwd=" + password + "; database=" + defdb
    try:
        connection.Open(constr)
        if connection.State == adStateOpen:
            pass
    except Exception as inst:
        print('Exception in SqlConnect2:', inst)
        return -1

    #now we execute--------------------------------------------------------------------
    try:
        recordset = connection.execute(sqlquery)
    except Exception as inst:
        print('Exception in SqlExecute2:', inst)
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

    connection.Close
    return records, fieldnames

#working here

def SqlExecute3(servername = '',username = '',password = '', defdb = 'master', sqlquery=''):
    connection = win32com.client.Dispatch(r'ADODB.Connection')
    # Connection State Constants
    #
    adStateClosed	    = 0
    adStateOpen	        = 1
    adStateConnecting	= 2
    adStateExecuting	= 4
    adStateFetching	    = 8
    colseparator = chr(1)
    if username == '':
        constr = "sqlcmd -E -S" + servername + " -d" + defdb + " /w 8192 -W " + ' -s' + colseparator + '  '
    else:
        constr = "sqlcmd -U" + username + " -P" + password + " -S" + servername + " -d" + defdb + " /w 8192 -W " + ' -s' + colseparator + '  '

    # try:
    #     connection.Open(constr)
    #     if connection.State == adStateOpen:
    #         pass
    # except Exception as inst:
    #     print('Exception in SqlConnect2:', inst)
    #     return -1

    #now we execute--------------------------------------------------------------------
    try:
        #recordset = connection.execute(sqlquery)
        data = os.popen(constr + '-Q"' + sqlquery + '"').readlines()
    except Exception as inst:
        print('Exception in SqlExecute3:', inst)
        return -1

    records = []
    fieldnames = data[0].strip().split(colseparator)
    #data[0] column names
    #data[1] dashed lines, skip
    #data[2:]

    for x in range(len(data[2:])):
        records.append(data[x + 2].strip().split(colseparator))
    #     fieldnames.append(recordset.Fields.Item(x).Name)
    #     #Need the try for not select type of sql, like updates, inserts
    # values_list = []
    # try:
    #     data = recordset.GetRows()
    #     rowcount = len(data[0])
    #     for y in range(0, rowcount):
    #         for x in data:
    #             values_list.append(x[y])
    #         records.append(tuple(values_list))
    #         values_list = []
    #     records = tuple(records)
    # except UnboundLocalError:
    #     pass
    # except:
    #     pass
    #
    # connection.Close
    #return records, fieldnames
    return records, fieldnames









if __name__ == '__main__':

    conn = SqlConnect('(local)\sql2014',username = '',password = '', defdb = 'AdventureWorks2012')

    #testing select query
    rows, fnames = SqlExecute(conn, 'select top 10  * from Person.Person')
    print(fnames)
    for x in rows:
        print(x)

    #testing update query
    FirstName = 'Keny'
    BusinessEntityID = '1'
    rows, fnames = SqlExecute(conn, "update Person.Person set FirstName ='" + FirstName + "' where BusinessEntityID = " + BusinessEntityID)
    print('Reading record')
    rows, fnames = SqlExecute(conn, 'select * from Person.Person where BusinessEntityID = 1')
    print(rows)


    print('Test of SqlExecute2')
    rows, fnames = SqlExecute2('(local)\sql2014',username = '',password = '', defdb = 'AdventureWorks2012', sqlquery ='select top 10  * from Person.Person')
    print(fnames)
    for x in rows:
        print(x)

    conn = SqlConnect('CCLTSTECOSQLDB1\\TSTECOSQL1',username = '',password = '', defdb = 'EARLY_BOARDING')

    #testing select query
    rows, fnames = SqlExecute(conn, 'select top 10  * from sysusers')
    print(fnames)
    for x in rows:
        print(x)

    rows, fnames = SqlExecute(conn, sqlsynclogins)
    print(fnames)
    for x in rows:
        print(x)

    print('testing sqlexecute3')
    x, f = SqlExecute3('(local)\sql2014',username = '',password = '', defdb = 'AdventureWorks2012', sqlquery ='set nocount on select top 10  * from Person.Person')
    #print(x)
    for g in x:
         print(g)

    print(f)
    for g in f:
         print(g)