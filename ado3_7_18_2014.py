import win32com.client

def connect(qry):
	con=win32com.client.Dispatch('ADODB.Connection')
	rs=win32com.client.Dispatch('ADODB.recordset')
	con.Open("Provider=SQLOLEDB.1;Data Source=localhost\sql2014;Trusted_Connection=yes;database=AdventureWorks2012")
	sql=qry +";"
	rs=con.Execute(sql)
	con.Close
	return rs

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

connection = win32com.client.Dispatch(r'ADODB.Connection')
#DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=c:\\pfad\\testdb.mdb;'
DSN = "Provider=SQLOLEDB.1;Data Source=localhost\sql2014;Trusted_Connection=yes;database=AdventureWorks2012"
connection.Open(DSN)
recordset = win32com.client.Dispatch(r'ADODB.Recordset')
recordset.Open('select top 10 * from Person.Person', connection, 1, 3)
fields_dict = {}
fields_list = []
values_list = []
out_list = []
for x in range(recordset.Fields.Count):
    #fields_dict[x] = recordset.Fields.Item(x).Name
    fields_list.append(recordset.Fields.Item(x).Name)
data = recordset.GetRows()
rec_count = len(data[0])
print('records: ' + str(rec_count))
print('===============')
print (fields_list)
for y in range(0, rec_count):
    for x in data:
        values_list.append(x[y])
    out_list.append(values_list)
#    print(values_list)
    values_list = []
    #print (fields_dict[x], recordset.Fields.Item(x).Value)
    #values_list.append(recordset.Fields.Item(x).Value)
    #print (fields_dict[x])
    #if x == 0:
    #    print (fields_list)
    #print(values_list)

print(out_list)
for x in out_list:
    print(x)

# import win32com.client
#
# connection = win32com.client.Dispatch(r'ADODB.Connection')
# DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=c:\\pfad\\testdb.mdb;'
# connection.Open(DSN)
# recordset = win32com.client.Dispatch(r'ADODB.Recordset')
# recordset.Open('SELECT * FROM Auftraege', connection, 1, 3)
# fields_dict = {}
# for x in range(recordset.Fields.Count):
#     fields_dict[x] = recordset.Fields.Item(x).Name
#     print fields_dict[x], recordset.Fields.Item(x).Value


# def ado():
#     '''
#     connect with com dispatch objs
#     '''
#     conn = win32com.client.Dispatch(r'ADODB.Connection')
#     DSN = ('PROVIDER = Microsoft.Jet.OLEDB.4.0;DATA SOURCE = ' + db +  ';')
#     conn.Open(DSN)
#
#     rs = win32com.client.Dispatch(r'ADODB.Recordset')
#     strsql = "select * from deer"
#     rs.Open(strsql, conn, 1, 3)
#     t = rs.GetRows()
#     conn.Close()
#     return t