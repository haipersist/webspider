import datetime
from baseclass.send_email import SendMail
from baseclass.utils.data2html import data2html
from baseclass.utils.store_data import Job_Data
from gen_data.gen_daily_job import get_latest_data
from gen_data.get_good_job import  GoodJob

def send_daily_data():
    jobdata = get_latest_data()
    store_job = Job_Data(store_type='redis')
    store_job.store(jobdata)
    result = data2html(jobdata,'job.tpl')
    mail = SendMail('Job')
    try:
        mail.send_email(msghtml=result)
    except:
        mail.send_email(msghtml=result)



def send_good_job():
    gjob = GoodJob()
    renderg = gjob.get_renderg()
    huaxia = gjob.get_huaxia()
    data = []
    if renderg:
        data.extend(renderg)
    if huaxia:
        data.extend(huaxia)
    if data:
        result = data2html(data,'job.tpl')
        mail = SendMail('Job')
        try:
            mail.send_email(msghtml=result)
        except:
            mail.send_email(msghtml=result)
    else:
        print '%s:No job info about the companies' % datetime.date.today().strftime("%Y-%m-%d")


if __name__ == "__main__":
    send_daily_data()
    send_good_job()


