def SqlExecute(conn, sqlquery=''):

    """
    Executes sqlquery and returns lists with column names and data
    The connection info is passed as a dictionary with these required keys:
    servername, username,password
    If username is empty will use integrated security
    These keys are optional: defdb, colseparator
    """
    import subprocess

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


def SqlExecuteDict(conn, sqlquery=''):

    """
    Executes sqlquery and returns a dictionary
    The connection info is passed as a dictionary with these required keys:
    servername, username,password
    If username is empty will use integrated security
    These keys are optional: defdb, colseparator
    """
    import subprocess

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

    print(r"Let's make a dictionary with the total output")
    dict = {}
    seq = 0
    cnt = len(data)
    lst = []
    for x in fieldnames:
        dict[x] = []
        for y in data:
            dict[x].append(y[seq])
        seq = seq + 1

    return dict







'''
def SqlExecute(conn, sqlquery=''):

    import subprocess

    if 'colseparator' not in conn.keys():
        conn['colseparator'] = chr(1)
    if conn['username'] == '':
        constr = "sqlcmd -E -S" + conn['servername'] + "  /w 8192 -W " + ' -s' + conn['colseparator'] + '  '
    else:
        constr = "sqlcmd -U" + conn['username'] + " -P" + conn['password'] + ' -S' + conn['servername'] + '  /w 8192 -W  -s' + conn['colseparator'] + '  '


    data = subprocess.Popen(constr + '-Q"' + sqlquery + '"', stdout=subprocess.PIPE).communicate()


    records = []
    lst = data[0].splitlines()
    # lst[0] column names;  lst[1] dashed lines, (skip); lst[2:] data
    # now we decode
    for x in lst:
        line = x.decode()
        lst2 = line.split(conn['colseparator'])
        records.append(lst2)
    fieldnames = records[0]
    data = records[2:]

    return data, fieldnames

'''
