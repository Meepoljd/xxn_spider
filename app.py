import requests
import time
import smtplib
import email.mime.text
from lxml import etree
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def main():
    scheduler = BlockingScheduler()
    # 或者interval
    scheduler.add_job(crawler, 'cron', day_of_week='1-5', hour='6')
    scheduler.start()

def crawler():
    r = requests.get("http://www.csrc.gov.cn/pub/newsite/fxjgb/fshgg/")
    html = etree.HTML(r.text)
    news = html.xpath("//ul[@id='myul']/li")
    today = '\n' + datetime.now().strftime("%Y-%m-%d")
    for n in news:
        if today == n.xpath("./span/text()")[0]:
            url = n.xpath("./a/@href")[0]
            url = "http://www.csrc.gov.cn/pub/" + url[9:]
            tmp = requests.get(url)
            dom = etree.HTML(tmp.content)
            main = dom.xpath("//div[@class='main']")[0]
            msg = etree.tostring(main, pretty_print=True)
            main(msg)

def mail(content):
    mail_username = 'xxx@gmail.com'
    mail_password = 'password'
    from_addr = mail_username
    to_addrs = ('xxx@gmail.com')

    # HOST & PORT
    HOST = 'smtp.gmail.com'
    PORT = 25
    smtp = smtplib.SMTP()

    try:
        smtp.connect(HOST, PORT)
    except:
        pass
    smtp.starttls()
    # login with username & password
    try:
        smtp.login(mail_username, mail_password)
    except:
        pass
    msg = email.mime.text.MIMEText(content, "html")
    msg['From'] = from_addr
    msg['To'] = ';'.join(to_addrs)
    msg['Subject'] = 'Subject'
    smtp.sendmail(from_addr, to_addrs, msg.as_string())
    smtp.quit()

if __name__ == '__main__':
    crawler()
