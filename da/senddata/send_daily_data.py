from datetime import date
from webspider.baseclass.send_email import Mail
from webspider.utils.data2html import data2html
from webspider.da.GetDailyJobs import DailyJob
from webspider.da.GetNewCompany import NewCompany
from webspider.utils.get_project_setting import Settings
from da.GetSeridJobs import SeridJob



class SendData(object):

    def __init__(self):
        self.mail = Mail('daily')
        self.mon_mail = Mail('monthly')
        self.day = date.today().strftime("%Y-%m-%d")

    def send_daily_job(self,day=None):
        day = self.day if day is None else day
        job = DailyJob(day)
        result = job.get_daily_job()[0:30]
        total = len(job.get_daily_job())
        #convert job list into html
        html = data2html('job.tpl',data=result,total=total)
        print html
        self.mail.send_email(msghtml=html)

    def send_daily_company(self):
        com = NewCompany()
        companies = com.daily_new_company
        if len(companies) != 0:
            html = data2html('company.tpl', data=companies, total=len(companies))
            self.mail.send_email(msghtml=html)

    def exec_all(self):
        for item in dir(self):
            if item.startswith('send'):
                apply(getattr(self, item))

    def stat_by_company(self,serid=30):
        serid = SeridJob(serid=serid)
        result = serid.get_serid_job_groupby('company',serid.start,serid.end)
        result = sorted(result.items(),key=lambda x:x[1],reverse=True)
        html = data2html('month_by_company.tpl', data=result)
        self.mon_mail.send_email(msghtml=html)

    def stat_by_website(self,serid=30):
        serid = SeridJob(serid=serid)
        result = serid.get_serid_job_groupby('website',serid.start,serid.end)
        result = sorted(result.items(),key=lambda x:x[1],reverse=True)
        html = data2html('month_by_website.tpl', data=result)
        self.mon_mail.send_email(msghtml=html)


if __name__ == "__main__":
    s = SendData()
    #s.send_daily_company()
    s.send_daily_job()




