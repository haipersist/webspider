#!/usr/bin/env python
#encoding:utf8

import email
import time
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
import smtplib
import os
import sys
import ConfigParser
import ast
import commands
from webspider.utils.get_project_setting import get_project_setting


class Mail():

    def __init__(self,obj):
        self.obj =obj
        self.path = os.environ.get('SPIDERPATH')
        self._set_server()
        self._set_config()

    def _set_server(self):
        setting = get_project_setting()
        self.email_var = setting['EMAIL']
        self.send_server = self.email_var['EMAIL_HOST']
        self.user = self.email_var['EMAIL_HOST_USER']
        self.port = self.email_var['EMAIL_PORT']
        self.password = self.email_var['EMAIL_HOST_PASSWORD']
        self.smtp = smtplib.SMTP(self.send_server)

    def _set_config(self):
        cfg_path = os.path.join(self.path,'config')
        filepath = os.path.join(cfg_path,'sendemail.cfg')
        self.cfg = ConfigParser.ConfigParser()
        self.cfg.read(filepath)
        self.to_addrs =ast.literal_eval(self.cfg.get(self.obj,'addrs'))
        self.subject = self.cfg.get(self.obj,'subject')

    def send_email(self,msgtxt=None,filename=None,msghtml=None):
        ms = MIMEMultipart()
        Addrs = [email.utils.formataddr((False,addr)) for addr in self.to_addrs]
        ms['To'] = ','.join(Addrs)
        ms['From'] = self.user
        ms['Subject'] = self.subject
        ms['Date'] = email.utils.formatdate(time.time(),True)
        #ms.attach(MIMEText(self.txt))
        if msgtxt:
            ms.attach(MIMEText(msgtxt,'plain','utf8'))

        if msghtml is not None:
            ms.attach(MIMEText(msghtml,'html','utf8'))
   
        if filename:
            attat = MIMEText(file(filename,'rb').read(),'base64','utf8')
            attat["Content-Type"]='application/octet-stream'
            attat['Content-Disposition']='attatcnment;filename="%s" '%filename
            ms.attach(attat)
        
        self.smtp.login(self.user,self.password)
        try:
            self.smtp.sendmail(ms['From'],Addrs,ms.as_string())
            self.smtp.quit()
            print 'send success'
            return
        except Exception,e:
            print str(e)




if __name__=="__main__":
    S_mail = Mail('myself')
    S_mail.send_email(msgtxt='send_email')


