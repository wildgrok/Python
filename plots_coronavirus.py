# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.area.html
# created from plots.py 11/14/2020


import pandas as pd
# import matplotlib
import matplotlib.pyplot as plt
#pd.options.plotting.backend
from dblib3 import *
# import dblib3


df = pd.DataFrame({
    'sales': [3, 2, 3, 9, 10, 6],
    'signups': [5, 5, 6, 12, 14, 13],
    'visits': [20, 42, 28, 62, 81, 50],
}, index=pd.date_range(start='2018/01/01', end='2018/07/01',
                       freq='M'))
ax = df.plot.area()
ax.plot()
df.plot()
# plt.show()
plt.savefig("c://DOWNLOADS/plot.jpg")
# print(ax)
# matplotlib.validate_backend

c = Connection('WORKSTATION\SQLEXPRESS', db='coronavirus')
print("Connection string: " + c.constr)
if c.connected == 1:
     print("Connected OK")

cu = c.cursor
s = 'SELECT [Province_State],[Country_Region],[Last_Update],[Deaths] '
s = s + 'FROM [coronavirus].[dbo].[data_usa2] '
s = s + 'where Province_State =' + chr(39) + 'Florida' + chr(39)
print(s)
lst = cu.execute(s)
print('rowcount=' + str(cu.rowcount))
rows = cu.fetchall()
for x in rows:
    print(x)
c.close()