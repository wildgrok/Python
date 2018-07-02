# mail.py


# --------------section for sendmail---------------------------------------
import smtplib;
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText;
from email.mime.multipart import MIMEMultipart;


# create msg - MIME* object
# takes addresses to, from cc and a subject
# returns the MIME* object
def create_msg(to_address,
               from_address='',
               cc_address='',
               bcc_address='',
               subject=''):
    
    msg = MIMEMultipart();
    msg['Subject'] = subject;
    msg['To'] = to_address;
    msg['Cc'] = cc_address;
    msg['From'] = from_address;
    return msg;

# send an email
# takes an smtp address, user name, password and MIME* object
# if mode = 0 sends to and cc
# if mode = 1 sends to bcc
def send_email(smtp_address, usr, password, msg, mode):
    server = smtplib.SMTP(smtp_address);
    server.ehlo();
    # server.starttls();
    server.ehlo();
    server.login(username,password);
    if (mode == 0 and msg['To'] != ''):
        server.sendmail(msg['From'],(msg['To']+msg['Cc']).split(","), msg.as_string());
    elif (mode == 1 and msg['Bcc'] != ''):
        server.sendmail(msg['From'],msg['Bcc'].split(","),msg.as_string());
    elif (mode != 0 and mode != 1):
        print('error in send mail bcc'); print('email cancelled'); exit();
    server.quit();

# compose email
# takes all the details for an email and sends it
# address format: list, [0] - to
#                       [1] - from (ADDED)
#                       [2] - cc
#                       [3] - bcc
# subject format: string
# body format: list of pairs [0] - text
#                            [1] - type:
#                                        0 - plain
#                                        1 - html
# files is list of strings
def compose_email(addresses, subject, body, files):

    # addresses
    to_address = addresses[0];
    from_address = addresses[1];
    cc_address = addresses[2];
    bcc_address = addresses[3];


    # create a message
    msg = create_msg(to_address, from_address=from_address, cc_address=cc_address , subject=subject);

    # add text
    for text in body:
        attach_text(msg, text[0], text[1]);

    # add files
    if (files != ''):
        file_list = files.split(',');
        for afile in file_list:
            attach_file(msg, afile);

    # send message
    send_email(server, username, password, msg, 0);

    # check for bcc
    if (bcc_address != ''):
        msg['Bcc'] = bcc_address;
        send_email(server, username, password, msg, 1);
        
    print('email sent')

# attach text
# attaches a plain text or html text to a message
def attach_text(msg, atext, mode):
    part = MIMEText(atext, get_mode(mode));
    msg.attach(part);

# util function to get mode type
def get_mode(mode):
    if (mode == 0):
        mode = 'plain';
    elif (mode == 1):
        mode = 'html';
    else:
        print('error in text kind'); print('email cancelled'); exit();
    return mode;

# attach file
# takes the message and a file name and attaches the file to the message
def attach_file(msg, afile):
    part = MIMEApplication(open(afile, "rb").read());
    part.add_header('Content-Disposition', 'attachment', filename=afile);
    msg.attach(part);

#to be tested...
# compose_email(['cpt@thelivingpearl.com','',''],
#               'EMAILSENDER@mail.com',
#               'test v.5.0',
#               [['some text goes here...\n',0]],
#               '');
              
#compose_email can take the following arguments: 
#	1. to recipients (separated by a comma)
#   2. from (single value)
#	3. cc recipients (separated by a comma)
#	4. bcc recipients (separated by a comma)
#	5. subject
#	6. a list with message and mode (plain txt or html)
#	7. files to be attached

# ------------------end of section for sendmail---------------------------------

# =========================getmail===============================
#, '- See more at: http://www.codemiles.com/python-tutorials/reading-email-in-python-t10271.html')#sthash.A6Qkggmj.dpuf

def get_emails(username,password,server):

    import poplib

    pop_conn = poplib.POP3_SSL(server)
    pop_conn.user(username)
    pop_conn.pass_(password)

    #Get messages from server:
    return [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]




# =========================getmail end ===============================


if __name__ == '__main__':

    #account setup
    username = 'mailman@besada.com';
    password = 'camello1';
    #server = 'smtp.gmail.com:587';
    server = 'besada.com';




    import poplib
    import time



    lst = []

    sentfile = '/home/python/sentfile.txt'


    while True:
        print("---------")

        # pop_conn = poplib.POP3_SSL('besada.com')
        # pop_conn.user('mailman@besada.com')
        # pop_conn.pass_('camello1')

        #Get messages from server:
        #messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
        messages = get_emails(username,password,server)

        for message in messages:

            s = ''
            s2 = ''
            s3 = ''
            print('--------------------')
            for x in message[1]:
                if x[0:5].decode('utf-7') == 'From:':
                    s2 = x[5:].decode('utf-7')         #s2 is from

                    #print(s2)
                if x[0:8].decode('utf-7') == 'Subject:':
                    s = x[8:].decode('utf-7')
                    #print(s)
                    if s.strip() == 'PYTHON ROCKS':
                        s3 = s.strip()                 #s3 is PYTHON ROCKS

            if (s2 > '') and (s3 > ''):
                with open(sentfile, 'r') as file:
                    for line in file:
                        lst.append(line.rstrip())
                theset = set(lst)
                if s2 in theset:
                    pass
                else:
                    print('emails: ', theset)
                    compose_email([s2,'noreply@besada.com','',''],'PYTHON ROCKS',[['You have graduated from the Python course ... show your pride...\n',0]],'');
                    with open(sentfile, 'a') as file2:
                        file2.write(s2 + "\n")

        time.sleep(5)
        print("---------\n")


