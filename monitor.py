
import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText



def send_sms(content):
    email_host = "smtp.163.com"
    email_port = 465
    email_sender = ""
    password = ''
    email_receiver = ["",""]
    email_cc = []
    msg = MIMEText(content, 'plain', 'utf-8')
    msg["Subject"] = "邮件的主题"  # 邮件主题描述
    msg["From"] = email_sender  # 发件人显示,不起实际作用,只是显示一下
    msg["To"] = ",".join(email_receiver)  # 收件人显示,不起实际作用,只是显示一下
    msg["Cc"] = ",".join(email_cc)  # 抄送人显示,不起实际作用,只是显示一下
    with smtplib.SMTP_SSL(email_host, email_port) as smtp:  # 指定邮箱服务器
        smtp.login(email_sender, password)  # 登录邮箱
        smtp.sendmail(email_sender, email_receiver, msg.as_string())  # 分别是发件人、收件人、格式
        smtp.quit()
    print("发送邮件成功!")

def getMoreinfoKS():
    try:
        datafile = 'data.txt'
        with open(datafile, 'r',encoding="utf-8") as f:
            old_response = f.read()
            # print(old_response)
            f.close()
        url = 'http://www.hbsrsksy.cn/hbksy/001/001001/moreinfoKS.html'
        # 监控信息源地址
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Referer":"http://www.hbsrsksy.cn/hbksy/001/001002/ksjh.html"}
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = soup.find_all('ul', class_='ewb-info-items')
        news_list_lis = news_list[0].find_all('li')
        for news_list_li in news_list_lis:
            news_title = news_list_li.find('a').get_text().split('>')[-1].strip()
            news_url = 'http://www.hbsrsksy.cn' + news_list_li.find('a')['href'].strip()
            news_time = news_list_li.find('span',class_="ewb-date").get_text().strip()
            # 返回最新的招录聘考试文件信息
            # print(news_title,news_url,news_time)
            if news_url not in old_response:
                print(news_title, news_url, news_time)
                time.sleep(2)
                content = "获取到一条湖北考试信息网更新：\ntitle:{title}\nurl:{url}\ntime:{time}".format(title=news_title,url=news_url,time=news_time)
                send_sms(content)
                with open(datafile,"a+",encoding="utf-8") as w:
                    w.write(news_title + "," + news_url + "," + news_time + "\n")
                        # w.write(news_title+","+news_url+","+news_time+"\n")

            # print('-'*1000)
            # return news_title, news_url
        # print(result)
    except Exception as e:
        print(e)
        getMoreinfoKS()


if __name__ == '__main__':
    # send_sms('test')
    i = 1
    while True:
        print("程序正在运行，当前第"+str(i)+"次循环")
        i+=1
        getMoreinfoKS()
        time.sleep(1000)