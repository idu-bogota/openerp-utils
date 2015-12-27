import smtpd
import asyncore
from email.parser import Parser
import base64
import datetime
import webbrowser
import os
import tempfile

class CustomSMTPServer(smtpd.SMTPServer):
    def __init__(*args, **kwargs):
        print "Running fake smtp server on port 1025"
        smtpd.SMTPServer.__init__(*args, **kwargs)

    def process_message(self, peer, mailfrom, rcpttos, data):
        print """

///////////////////////////////////////////////////////
=======================================================
"""
        print 'Received at', datetime.datetime.now()
        print 'Receiving message from:', peer
        print 'Message addressed from:', mailfrom
        print 'Message addressed to  :', rcpttos
        print 'Message length        :', len(data)
        msg = Parser().parsestr(data)
        for part in msg.walk():
            if part.get_content_type() in ['text/html']:
                filename = '/tmp/message.%s.html' % datetime.datetime.now()
                temp = open(filename, 'w+b')
                try:
                    temp.write(base64.b64decode(part.get_payload()))
                    webbrowser.open_new_tab(temp.name)
                finally:
                    # Automatically cleans up the file
                    temp.close()

            if part.get_content_type() in ['text/plain', 'text/html']:
                print """

*******************************************************
=======================================================
"""
                print base64.b64decode(part.get_payload())
                print """
=======================================================
*******************************************************

"""


server = CustomSMTPServer(('127.0.0.1', 1025), None)

asyncore.loop()
