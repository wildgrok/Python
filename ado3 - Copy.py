# import win32com.client
#
# def connect(qry):
# 	con=win32com.client.Dispatch('ADODB.Connection')
# 	rs=win32com.client.Dispatch('ADODB.recordset')
# 	con.Open("Provider=SQLOLEDB.1;Data Source=localhost\sql2014;Trusted_Connection=yes;database=AdventureWorks2012")
# 	sql=qry +";"
# 	rs=con.Execute(sql)
# 	con.Close
# 	return rs

# def display (NUM_ROWS):
# 	print "<table border=1>"
# 	print "<th>Order ID</th>"
# 	print "<th>Product</th>"
# 	print "<th>Unit Price</th>"
# 	print "<th>Quantity</th>"
# 	print "<th>Discount</th>"
# 	for k in range(0,NUM_ROWS):
# 		print "<tr>"
# 		for i in s:
# 			print "<td>",i[k],"</td>"
# 		print "</tr>"
#
# 	print "</table>"
#
# #rs=win32com.client.Dispatch('ADODB.recordset')
# rs = connect("select top 10 * from Person.Person")
# #s=rs[0].GetRows(NUM_ROWS)
# s = rs[0].GetRows()
# #display(NUM_ROWS)
# #rs.Close
# for k in range(0,10):
#  	print ("<tr>")
#  	for i in s:
#  		print ("<td>",i[k],"</td>")
#  	print ("</tr>")



import win32com.client
#from win32com.client import constants
from adoconstants import *
connection = win32com.client.Dispatch(r'ADODB.Connection')


class Connection:
    def __init__(self, servername, username='', password='', db=''):
        self.version = '';
        self.servername = servername;
        self.username = username;
        self.password = password;
        self.defdb = db;
        self.constr = '';
        if db == '':
            self.defdb = 'master'
        self.connected = 0

        if username == '':
            self.constr = "Provider=SQLOLEDB.1;Data Source=" + self.servername + ";Trusted_Connection=yes; database=" + self.defdb
        else:
            self.constr = "Provider=SQLOLEDB.1;Data Source=" + self.servername + ";uid=" + username + ";pwd=" + password + "; database=" + self.defdb

        #test connection:
        s = "set nocount on select name from master..syslogins where name = 'sa'"
        connection.Open(self.constr)
        if connection.State == adStateOpen:
            self.connected = 1


        try:
            #if lst[2].strip() == 'sa':
            #    self.connected = 1
            #else:
            #    self.connected = 0
            c = Cursor()
            c.servername = servername
            c.username = username
            c.password = password
            c.defdb = db
            c.constr = self.constr
            self.cursor = c
        except IndexError:
            self.connected = 0
            print("Could not connect")

    def commit(self):
        "this is here for compatibility"
        pass

    def close(self):
        self = None
        return self




class Cursor:
    def __init__(self):
        self.defdb = ''
        self.servername = ''
        self.username = ''
        self.password = ''
        self.constr = ''
        self.rowcount = -1
        self.records = []
        self.rowid = 0
        self.sql = ''
        self.colseparator = chr(1)  #default column separator
        #this is going to be a list of lists, each one with:
        #name, type_code, display_size, internal_size, precision, scale, null_ok
        self.description = []
        self.fieldnames = []
        self.fieldvalues = []
        self.fieldvalue = []
        #one dictionary by column
        self.dictfield = {'name': '', 'type_code': 0, 'display_size': 0, 'internal_size': 0, 'precision': 0, 'scale': 0,
                          'null_ok': 0}
        #list of lists
        self.dictfields = []


    def execute(self,sql):
        self.records = []
        recordset = win32com.client.Dispatch(r'ADODB.Recordset')
        recordset.Open(sql, connection, 1, 3)
        values_list = []
        #out_list = []
        for x in range(recordset.Fields.Count):
            self.fieldnames.append(recordset.Fields.Item(x).Name)
        data = recordset.GetRows()
        self.rowcount = len(data[0])
        for y in range(0, self.rowcount):
            for x in data:
                values_list.append(x[y])
            self.records.append(tuple(values_list))
            values_list = []
        self.records = tuple(self.records)


    def fetchall(self):

        lst = []
        try:
            for x in self.records:
                lst.append(x)
        except IndexError:
            pass
        return lst

    def fetchone(self):
        i = self.rowid
        j = i + 1
        self.rowid = j
        try:
            return tuple(self.records[i])
        except IndexError:
            pass


if __name__ == '__main__':
    c = Connection('(local)\sql2014', db='AdventureWorks2012')
    print("Connection string: " + c.constr)
    if c.connected == 1:
        print("Connected OK")
    cu = c.cursor
    lst = cu.execute('select top 10  * from Person.Person')
    print("list of columns:")
    print(cu.fieldnames)
    print('rowcount=' + str(cu.rowcount))
    rows = cu.fetchall()
    for x in rows:
        print(x)

    print('Bringing records one by one')
    cu.rowid = 5
    rows = cu.fetchone()
    print(rows)
    rows = cu.fetchone()
    print(rows)


    c.close()