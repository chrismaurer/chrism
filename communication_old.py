###########################################################################
#    
#      Copyright (c) 2007 Trading Technologies International, Inc.
#                     All Rights Reserved Worldwide
#
#        * * *   S T R I C T L Y   P R O P R I E T A R Y   * * *
#
# WARNING:  This file is the confidential property of Trading Technologies
# International, Inc. and is to be maintained in strict confidence.  For
# use only by those with the express written permission and license from
# Trading Technologies International, Inc.  Unauthorized reproduction,
# distribution, use or disclosure of this file or any program (or document)
# derived from it is prohibited by State and Federal law, and by local law
# outside of the U.S. 
#
###########################################################################
# $RCSfile: src/pyfmds/utils/communication.py $
# $Date: 2008/08/27 13:21:03CDT $
# $Author: Brian Curtin (bcurtin) $
# $Revision: 1.5 $
###########################################################################


from smtplib import SMTP
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from types import ListType

class Email(object):

    Subject = 'results_2010-02-02_160025.txt'
    Sender = 'Chris Maurer (TT)'
    Recipient = 'chris.maurer@tradingtechnologies.com'
    BodyText = None
    HTMLText = None
    Attachment = r'C:\temp\logs\results_2010-02-02_160025.txt'
    SMTPServer = 'mail.int.tt.local' #valid as of 2008-05-21
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            
        if hasattr(self, 'Recipient'):
            self.BuildMultisenderList()
            
    def Send(self):
        '''
        Using SMTP, create and send the email message
        '''
        msg = MIMEMultipart()
        msg['Subject'] = self.Subject
        msg['From'] = self.Sender
        msg['To'] = self.Recipient
        msg.preamble = self.BodyText
        
        if self.Attachment:
            attachment = MIMEText(self.Attachment, _subtype='plain')
            attachment.add_header('content-disposition',
                                  'attachment',
                                  filename=self.Attachment)
            msg.attach(attachment)
            
        msg.attach(MIMEText(self.HTMLText, 'plain')) 
        smtp = SMTP(self.SMTPServer)
        smtp.sendmail(self.Sender, self.Recipient, msg.as_string())
        smtp.close()
        
    def BuildMultisenderList(self):
        '''
        If the user creates the Email class with a string
        for the recipient, then use it, otherwise join the list
        to a comma-separated string
        '''
        #i dont really like how this is done,
        # but we only want to do it with lists
        if type(self.Recipient) == ListType:
            self.Recipient = ', '.join(self.Recipient)
            
            
if __name__ == '__main__':
    testmail = Email(Subject='results_2010-02-01_112342.txt', Recipient=['chris.maurer@tradingtechnologies.com'],
                     Sender='Chris Maurer (TT)', Attachment = r'C:\temp\logs\results_2010-02-02_160025.txt', BodyText=None,
                     HTMLText='What\'s that fucking smell!?')
    testmail.Send()

    #testmail2 = Email(Recipient='bcurtin', Subject='second test')
