import win32com.client

adoConn = win32com.client.Dispatch('ADODB.Connection')
#connect = "Provider=SQLOLEDB.1;Data Source=2ua2070dlj\sql2014;Initial Catalog=msdb;Integrated Security=SSPI;"
connect = 'Provider=SQLOLEDB.1;Data Source=ccltstecosqldb1\\tstecosql1;Initial Catalog=msdb;Integrated Security=SSPI;'

sql = '''
	SELECT sysjobs.name,
	hist.message + '(' + CAST(hist.run_date as varchar) + '-' + CAST(hist.run_time as varchar) + ')' as message
	FROM sysjobs, sysjobhistory as hist
	WHERE sysjobs.job_id = hist.job_id
	AND hist.run_status = 0
	AND hist.instance_id = (SELECT MAX(instance_id) FROM sysjobhistory WHERE sysjobhistory.job_id = sysjobs.job_id)
    '''

adoConn.Open(connect)
alog = adoConn.Execute(sql)
while not alog[0].EOF:
	task=alog[0].Fields(0).Value
	entry=alog[0].Fields(1).Value
	print('<TR>\n')
	print('<TD VALIGN=top><FONT FACE="COURIER" SIZE=2>%s</FONT></TD>\n' % (task))
	print('<TD VALIGN=top><FONT FACE="COURIER" SIZE=2>%s</FONT></TD>\n' % (entry))
	print('</TR>\n')
	alog[0].MoveNext()
