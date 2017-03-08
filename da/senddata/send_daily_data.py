from datetime import date
from webspider.baseclass.send_email import Mail
from webspider.utils.data2html import data2html
from webspider.da.GetDailyJobs import DailyJob
from webspider.da.GetNewCompany import NewCompany


class SendData(object):

    def __init__(self):
        self.mail = Mail('myself')
        self.day = date.today().strftime("%Y-%m-%d")

    def send_daily_job(self,day=None):
        day = self.day if day is None else day
        job = DailyJob(day)
        total = job.total
        result = job.get_daily_job()[0:50]
        #convert job list into html
        html = data2html('job.tpl',data=result,total=total)
        print html
        self.mail.send_email(msghtml=html)

    def send_daily_company(self):
        com = NewCompany()
        companies = com.daily_new_company
        if len(companies) != 0:
            html = data2html('company.tpl', data=companies, total=len(companies))
        else:
            html='<h1>No new company!</h1>'
        self.mail.send_email(msghtml=html)

    def exec_all(self):
        for item in dir(self):
            if item.startswith('send'):
                apply(getattr(s, item))



if __name__ == "__main__":
    s = SendData()
    for item in dir(s):
        if item.startswith('send'):
            print item
            #print apply(getattr(s,item))



