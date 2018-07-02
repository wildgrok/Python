#Listing 17–4. Binary Download with Status Updates
#!/usr/bin/env python
# Advanced binary download - Chapter 17 - advbinarydl.py
import os, sys
from ftplib import FTP
# www.it-ebooks.info
# CHAPTER 17 ■ FTP
# 296

# Uploading Data
# File data can also be uploaded through FTP. As with downloading, there are two basic functions for
# uploading: storbinary() and storlines(). Both take a command to run, and a file-like object to
# transmit. The storbinary() function will call the read() method repeatedly on that object until its
# content is exhausted, while storlines(), by contrast, calls the readline() method.
# Unlike the corresponding download functions, these methods do not require you to provide a
# callable function of your own. (But you could, of course, pass a file-like object of your own crafting
# whose read() or readline() method computes the outgoing data as the transmission proceeds!)
# Listing 17–5 shows how to upload a file in binary mode.
# Listing 17–5. Binary Upload
#!/usr/bin/env python
# Binary download - Chapter 17 - binaryul.py
# from ftplib import FTP
# import sys, getpass, os.path
# if len(sys.argv) != 5:
# » print "usage: %s <host> <username> <localfile> <remotedir>" % (
# » » sys.argv[0])
# » exit(2)
# host, username, localfile, remotedir = sys.argv[1:]
# password = getpass.getpass(
# » "Enter password for %s on %s: " % (username, host))
# f = FTP(host)
# f.login(username, password)
# f.cwd(remotedir)
# fd = open(localfile, 'rb')
# f.storbinary('STOR %s' % os.path.basename(localfile), fd)
# fd.close()
# f.quit()
# This program looks quite similar to our earlier efforts. Since most anonymous FTP sites do not
# permit file uploading, you will have to find a server somewhere to test it against; I simply installed the
# old, venerable ftpd on my laptop for a few minutes and ran the test like this:
# $ python binaryul.py localhost brandon test.txt /tmp
# I entered my password at the prompt (brandon is my username on this machine). When the program
# finished, I checked and, sure enough, a copy of the test.txt file was now sitting in /tmp. Remember not
# to try this over a network to another machine, since FTP does not encrypt or protect your password!
# You can modify this program to upload a file in ASCII mode by simply changing storbinary() to
# storlines().





if os.path.exists('linux-1.0.tar.gz'):
    raise IOError('refusing to overwrite your linux-1.0.tar.gz file')
f = FTP('ftp.kernel.org')
f.login()
f.cwd('/pub/linux/kernel/v1.0')
f.voidcmd("TYPE I")
datasock, size = f.ntransfercmd("RETR linux-1.0.tar.gz")
bytes_so_far = 0
fd = open('linux-1.0.tar.gz', 'wb')
while 1:
    buf = datasock.recv(2048)
    if not buf:
        break
    fd.write(buf)
    bytes_so_far += len(buf)
    print("\rReceived", bytes_so_far)
    if size:
        print("of %d total bytes (%.1f%%)" % (size, 100 * bytes_so_far / float(size)))
    else:
        print("bytes")
    sys.stdout.flush()
print
fd.close()
datasock.close()
f.voidresp()
f.quit()

# There are a few new things to note here. First comes the call to voidcmd(). This passes an FTP
# command directly to the server, checks for an error, but returns nothing. In this case, the raw command
# is TYPE I. That sets the transfer mode to “image,” which is how FTP refers internally to binary files. In the
# previous example, retrbinary() automatically ran this command behind the scenes, but the lower-level
# ntransfercmd() does not.
# Next, note that ntransfercmd() returns a tuple consisting of a data socket and an estimated size.
# Always bear in mind that the size is merely an estimate, and should not be considered authoritative; the
# file may end sooner, or it might go on much longer, than this value. Also, if a size estimate from the FTP
# server is simply not available, then the estimated size returned will be None.
# The object datasock is, in fact, a plain TCP socket, which has all of the behaviors described in the
# first section of this book (see Chapter 3 in particular). In this example, a simple loop calls recv() until it
# has read all of the data from the socket, writing it out to disk along the way and printing out status
# updates to the screen.
