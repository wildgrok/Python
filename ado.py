__author__ = 'JorgeBe'


import win32com.client
#import pyodbc

def ado():
    '''
    connect with com dispatch objs
    '''
    conn = win32com.client.Dispatch('ADODB.Connection')
    #DSN = ('PROVIDER = Microsoft.Jet.OLEDB.4.0;DATA SOURCE = ' + db +  ';')
    #Server=myServerAddress;Database=myDataBase;Trusted_Connection=True;
    #Provider=SQLOLEDB.1;Data Source=192.168.1.100;Uid=username;Pwd=password;Database=dbname;
    DSN = ('Provider=SQLOLEDB.1;Server=localhost\sql2014;Database=' + db + ';Trusted_Connection=yes')

    conn.Open(DSN)

    rs = win32com.client.Dispatch('ADODB.Recordset')
    strsql = "select top 10  * from Person.Person"
    rs.Open(strsql, conn, 1, 3)
    t = rs.GetRows()
    conn.Close()
    return t



if __name__ == '__main__':

    db = 'AdventureWorks2012'
    data1 = ado()
    print(data1)
