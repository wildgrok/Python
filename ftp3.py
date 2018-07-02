__author__ = 'JorgeBe'

#!/usr/bin/env python
# Binary upload - Chapter 17 - binarydl.py


# -----------------Start of class ftp----------------------------------
import os
from ftplib import FTP


# class FtpTool:
#     def __init__(self, con, sendreceive, file, folder='', overwrite=1):
#         # import os
#         # from ftplib import FTP
#         self.con = con
#         self.sendreceive = sendreceive
#         self.file = file
#         self.folder = folder
#         self.overwrite = overwrite
#         self.f = FTP(self.con['server'])
#
#         if con['user'] > '':
#             self.f.login(con['user'], self.con['password'])
#         else:
#             self.f.login()
#         if folder > '':
#             self.f.cwd(self.folder)
#
#     def doftp(self):
#         if self.sendreceive == 'send':
#             fd = open(self.file, 'rb')
#             self.f.storbinary('STOR %s' % os.path.basename(self.file), fd)
#         else:
#             fd = open(self.file, 'wb')
#             self.f.retrbinary('RETR ' + self.file, fd.write)
#
#         fd.close()
#         self.f.quit()


def ftp_ops(con, sendreceive, file, folder='', overwrite=1):

    import os
    from ftplib import FTP
    if overwrite == 0:
        if os.path.exists(file):
            raise IOError('refusing to overwrite your ' + file + ' file')
    f = FTP(con['server'])

    if con['user'] > '':
        f.login(con['user'], con['password'])
    else:
        f.login()
    if folder > '':
        f.cwd(folder)

    if sendreceive == 'send':
        fd = open(file, 'rb')
        f.storbinary('STOR %s' % os.path.basename(file), fd)
    else:
        fd = open(file, 'wb')
        f.retrbinary('RETR ' + file, fd.write)

    fd.close()
    f.quit()


if __name__ == '__main__':

    con = {}

    con['user'] = ''
    con['password'] = ''
    con['server'] = 'ftp.kernel.org'

    file = 'patch8.gz'
    folder = '/pub/linux/kernel/v1.0'

    ftp_ops(con, 'receive', file, folder)
    #ftp_ops(con, 'receive', file, folder, 0)

    # gftp = FtpTool(con, 'receive', file, folder='', overwrite=1)
    # gftp.doftp()

    con['user'] = 'carnival'
    con['password'] = 'R7@C1rnv'
    con['server'] = 'ftp.riskconsole.com'

    file = 'DELETEME.txt'
    folder = '/CCL/Inbound/Lawson_Costs/'


    ftp_ops(con, 'send', file, folder)
    ftp_ops(con, 'send', file)

# open carnival:R7@C1rnv@ftp.riskconsole.com
# # Change the remote directory
# cd /CCL/Inbound/Lawson_Costs/
# lcd \\corpintranet\opconfiles\RMIS\OUT\
# # Upload the file to current working directory
# put *.gpg -nopreservetime -nopermissions
# # Disconnect
# close
# # Exit WinSCP
# exit