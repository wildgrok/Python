from sqlkit import *

CONNECTION = {}
CONNECTION['servername'] = r'localhost\sql2014'
CONNECTION['username'] = ''
CONNECTION['password'] = ''
CONNECTION['db'] = 'AdventureWorks2012'
print('The connection is a dictionary')
print(CONNECTION)

query = 'set nocount on select top 10 * from AdventureWorks2012.Person.Person'
print('This is our test query')
print(query)

# testing select query
rows, fnames = SqlExecute(CONNECTION, query)
print('these are the query columns in the first line')
print('followed by the data')
print(fnames)
for x in rows:
    print(x)

print(r"Let's make a dictionary with the total output")
dict = {}
seq = 0
cnt = len(rows)
lst = []
for x in fnames:
    dict[x] = []
    for y in rows:
        dict[x].append(y[seq])
    seq = seq + 1

#print(dict)
print('now we can do very cool things ')
all_first_names = dict['FirstName']
print(all_first_names)

print('This looks like a useful tool, so we create a copy of the SqlExecute named SqlExecuteDict with the extra code added')

dict = SqlExecuteDict(CONNECTION, query)
for x in dict.keys():
    print(x)
    for y in dict[x]:
        print('-------->', y)
