__author__ = 'JorgeBe'


#
# The way to use a Connection object is to first create the object, then set the various properties (depending on your database) and then call Open() to connect to the database. The ConnectionString property is the most important property of them all. Instead of setting individual properties like this:
#   oconn.Provider = "SQLOLEDB"
#   oconn.CommandTimeout = 60
# you can instead set all the properties in one shot with the ConnectionString property. All you need to do is separate each argument with a semicolon(;) character.
#   oconn.ConnectionString = "provider=SQLOLEDB; CommandTimeout=60; ... more properties ..."
# The ADO Connection piggybacks on top of other connection methods such as ODBC, OLE DB, RDS etc. Aside from the ConnectionString though, the other ADO components have no idea of what specific connection method is being used. This is one of the advantages of abstraction that ADO provides to the user.
#
#Now, on to some real Python code. We will assume we're connecting to SQL server for this example using OLEDB and then show some connection strings for other database engines. The code is very simple and the comments actually outweigh the code, so you should have no trouble understanding what is going on here.
# First import two useful modules
import win32com.client
from adoconstants import *

# Create the ADO Connection object via COM.
oConn = win32com.client.Dispatch('ADODB.Connection')
rs = win32com.client.Dispatch('ADODB.recordset')

# Now set the connection properties via the ConnectionString
# We're connecting to a SQL Server on 192.168.1.100 using OLEDB.
#oConn.ConnectionString = "Provider=SQLOLEDB.1;Data Source=192.168.1.100;" + \
#    "uid=my_user_name;pwd=my_password;database=my_database_name"

oConn.ConnectionString = "Provider=SQLOLEDB.1;Data Source=localhost\sql2014;Trusted_Connection=yes;database=AdventureWorks2012"

# Now open the connection
oConn.Open()

# Instead of setting the ConnectionString and then calling Open, it is also
# possible to call the Open method directly and pass the connection string
# as an argument to the method. {i.e.)
# oConn.Open("Provider=SQLOLEDB.1; Data Source=.....")

if oConn.State == adStateOpen:
  # Do something here
    print("We've connected to the database.")
    # Execute a stored procedure.
    rs.oConn.Execute("USP_Get_Person")
    # Execute an INSERT statement
    # oConn.Execute("INSERT INTO table(col1, col2) VALUES (2, 'Test String')")
    #rs = oConn.Execute("select top 10 * from Person.Person")
    print(oConn.State)
    print('count:')
    print(rs.count)



else:
    print ("We failed to connect to the database.")

# Close up the connection and unload the COM object
if oConn.State == adStateOpen:
    oConn.Close()
    print (oConn.State)
oConn = None

