import jira
import json,re,time
from jira import JIRA
from collections import Counter
import smtplib,time,os,sys
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from pypinyin import lazy_pinyin
from datetime import datetime

jira = JIRA('https://jira.99808.net',basic_auth=('starsliao', '6520sl'))
JQL = 'project = LIBRARY AND issuetype = 图书借阅 AND status = 借阅中'
issues = jira.search_issues(JQL)

def lend_bill():
    lend = {}
    for issue in issues:
        lend_date = re.match(('\d+-\d+-\d+'),issue.fields.updated).group()
        reporter = issue.fields.reporter.displayName
        component = issue.fields.components[0]
        content = component.name + ',' + lend_date
        if reporter in lend:
            lend[reporter].append(content)
        else:
            lend[reporter] = content.split('*') #在jira网页上手动输入的模块不需要按"空格\t"等分割，否则发邮件时借阅数量不对
    return lend

data = lend_bill()
number = {}
for k,v in data.items():
    if len(v) >= 2:
        number[k] = len(v)

def generate_tr(name, book):
    return '<tr><td>%s</td><td>%s</td></tr>' % (name, book)

def generate_html(data,type):
    if isinstance(list(data.values())[0],int):
        tds = [ generate_tr(name,count) for name,count in number.items() ]
    else:
        tds = [generate_tr(name,'   |   '.join(book)) for name, book in data.items()]

    html_ele = '''<!DOCTYPE html>
    <body>'''

    table_ele = '<table border="1" cellspacing="0" cellpadding="0" bordercolor="#006699" style="BORDER-COLLAPSE: collapse">'\
        + '\n' + '<tr bgcolor="#CCCCCC"><th width="85">借书人</th><th>%s</th><tr>' % type + '\n' \
        + '\n'.join(tds) + '</table>'


    html = html_ele + table_ele + '</body></html>'
    return html

#发送html
def sendhtml(data,subject=None,type=None,receiver='sunsw@blizzmi.com'):
    '''发送html'''
    smtpserver = 'smtp.163.com'
    username = 'shw_hnld'
    password = 'a10241010a'

    sender = 'shw_hnld@163.com'
    # receiver = 'sunsw@blizzmi.com'
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    subject = subject

    if isinstance(data,dict):
        msg = MIMEText(generate_html(data,type), _subtype='html')
    else:
        print('xxx')
        msg = MIMEText(data)
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = formataddr(['图书系统管理员',sender])
    msg['To'] = receiver
    smtp = smtplib.SMTP_SSL(smtpserver, 465)
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()

def sendto(name):
    name_list = lazy_pinyin(name)
    if len(name_list) == 2:
        email_name = name_list[0] + name_list[1]
    elif len(name_list) == 3:
        email_name = name_list[0] + name_list[1][0] + name_list[2][0]
    elif len(name_list) == 4:
        email_name = name_list[0] + name_list[1] + name_list[2][0] + name_list[3][0]
    email = email_name + '@blizzmi.com'
    return email

def expire():
    for issue in issues:
        created_time = issue.fields.created
        t = time.strptime(created_time[0:10], '%Y-%m-%d')
        lend_days = (datetime.now() - datetime(t.tm_year, t.tm_mon, t.tm_mday)).days

        if lend_days < 2:
            print('-->lend_days',lend_days)
            name = issue.fields.reporter.displayName
            book = issue.fields.components[0].name.split(' ')[1]
            sendhtml('《%s》离还书日还有%s天到期，请知悉。' % (book,30 - lend_days),subject='图书系统提示',receiver=sendto(name))

            if lend_days > 30:
                print('-->逾期名单', name)
                sendhtml('《%s》逾期未还，请及时归还。' % book, subject='图书系统提示', receiver=sendto(name))
                sendhtml('%s逾期未还书籍《%s》' % (name, book), subject='图书系统提示', receiver='sunsw@blizzmi.com')

def main():
    expire()
    for name,count in number.items():
        if count > 2:
            sendhtml('每人限借2本书籍，请勿超出，多余借出需在jira归还。',subject='图书系统提示',receiver=sendto(name))
            sendhtml('%s所借书籍超过2本' % name, subject='图书系统提示', receiver='sunsw@blizzmi.com')
    # sendhtml(number,subject='借书大于2本名单',type='借阅数量')
    # sendhtml(data,subject='未还书籍名单',type='未还书籍')

if __name__ == '__main__':
    main()