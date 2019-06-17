#!/usr/local/bin/python3.6
# -*- coding:utf-8 -*-
import hashlib,time,pymysql
from pypinyin import lazy_pinyin
from jira import JIRA
import requests,re
from bearychat import incoming
class register:
    def __init__(self, realname,level):
        realname = realname.strip()
        if len(realname) == 2:
            username = ''.join(lazy_pinyin(realname))
        elif len(realname) == 3:
            pyuname = lazy_pinyin(realname)
            username = pyuname[0]+pyuname[1][0]+pyuname[2][0]
        elif len(realname) == 4:
            pyuname = lazy_pinyin(realname)
            username = pyuname[0]+pyuname[1]+pyuname[2][0]+pyuname[3][0]
        else:
            print("no name")
        self.realname = realname
        self.email = username + '@blizzmi.com'
        self.passwd = hashlib.md5(bytes(username+'fromweb',encoding = "utf8")).hexdigest()[0:6]
        self.passwd_md5 = hashlib.md5(bytes(self.passwd,encoding = "utf8")).hexdigest()
        self.cookie = self.passwd_md5+hashlib.md5(bytes(str(time.time()),encoding = "utf8")).hexdigest()
        level_dict = {"测试":30,"开发":55,"PO":70,"运维":70}
        self.level = level
        if level in level_dict.keys():
            self.level_id = level_dict[level]
        else:
            self.level_id = 10
        self.username = username
        print(self.realname,self.username,self.email,self.passwd,self.cookie,level,self.level_id)

    def add_mantis(self):
        db = pymysql.connect("192.168.200.150","mantis","ZroXnQDlcJs7lgJ6", \
                             "mantis", use_unicode=True, charset="utf8mb4")
        cursor = db.cursor()
        sql = "INSERT INTO mantis_user_table (username, realname, email, password, \
               access_level, cookie_string,date_created) VALUES ('{}','{}','{}','{}', \
               '{}','{}','{}')".format(self.username, self.realname, self.email, self.passwd_md5, \
               self.level_id, self.cookie,int(time.time()))
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print("error")
        db.close()

    def add_jira(self):
        jira = JIRA('http://jira.blizzmi.local/',basic_auth=('starsliao', '6520sl'))
        checkuser = [i['fullname'] for i in jira.group_members('jira-software-users').values() if i['active'] is True and i['fullname'] == self.realname]
        if checkuser:
            return False
        else:
            jira.add_user(self.username,self.email,password=self.passwd,fullname=self.realname)
            if self.level in ("测试","开发","运维"):
                jira.add_user_to_group(self.username, '考勤组：研发运维测试技术支持')
            else:
                jira.add_user_to_group(self.username, '考勤组：PO美术行政其它')
            return True

    def add_doku(self,pro):
        data = {"do": "login", "id": "start", "p": "6520sl", "sectok": "", "u": "admin"}
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        s = requests.session()
        login = s.post("http://share.blizzmi.local/dokuwiki/doku.php?id=start",data = data,headers = header)
        tok = re.search("sectok=(.*)\"\s.*class",login.text).group(1)
        regdata = {
            "sectok": tok,
            "userid": self.username,
            "userpass": self.passwd,
            "userpass2": self.passwd,
            "username": self.realname,
            "usermail": self.email,
            "usergroups": 'user,' + pro,
            "do": 'admin',
            "page": 'usermanager',
            "start": '0',
            "fn[add]": '',
        }
        regdoku = s.post("http://share.blizzmi.local/dokuwiki/doku.php?id=start",data = regdata,headers = header)
        regdoku.status_code

    def sendbc(self,pro):
        data = {
                "text": "@何少东 @starsliao 新员工JIRA/Mantis/Doku账号自助创建成功，请开通以下[企业邮箱](https://portal.partner.microsoftonline.cn/Home)账号：\n姓名：{}（{}组：{}）：{}".format(self.realname,pro,self.level,self.email),
                "channel": "新入职员工安排",
        }
        resp = incoming.send("https://hook.bearychat.com/=bw8Sf/incoming/d485790fe1db5e65aba86ca0064ec3a1",data)
        print(resp.status_code)
        print(resp.text)


if __name__ == "__main__":
    new = register("大张伟","开发")
#    new.add_mantis()
#    new.add_jira()
#    new.add_doku("chess")
    new.sendbc("chess")
