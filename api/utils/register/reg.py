#!/usr/local/bin/python3.6
# -*- coding:utf-8 -*-
import hashlib,time,pymysql
from pypinyin import lazy_pinyin
from jira import JIRA
import requests,re
from bearychat import incoming
from jira.resources import User
from jira import client
from selenium import webdriver
from django.http.response import HttpResponse,JsonResponse
from jira.exceptions import JIRAError

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

    def del_mantis(self):
        print('\033[;34m删除mantis账户\033[0m')
        response_dict = {'name':'mantis','status':True,'error':None,'data':None}
        try:
            db = pymysql.connect("192.168.200.150","mantis","ZroXnQDlcJs7lgJ6", \
                                 "mantis", use_unicode=True, charset="utf8mb4")
            cursor = db.cursor()
            sql = "DELETE FROM mantis_user_table WHERE username = '{}'".format(self.username)
            print('-->sql', sql)
            cursor.execute(sql)
            db.commit()
            db.close()
            response_dict['data'] = 'mantis账号已删除'

        except pymysql.err.OperationalError as e:
            response_dict['status'] = False
            response_dict['error'] = "Can't connect to MySQL server"
        return response_dict

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

    # def add_doku(self, pro):
    #     data = {"do": "login", "id": "start", "p": "6520sl", "sectok": "", "u": "admin"}
    #     header = {"Content-Type": "application/x-www-form-urlencoded"}
    #     s = requests.session()
    #     login = s.post("http://share.blizzmi.local/dokuwiki/doku.php?id=start", data=data, headers=header)
    #     # print('-->login.text',login.text)
    #     tok = re.search("sectok=(.*)\"\s.*class", login.text).group(1)
    #     print('tok', tok)
    #
    #     login_url = "http://share.blizzmi.local/dokuwiki/doku.php?id=start"
    #     # opt = webdriver.ChromeOptions()
    #     # opt.set_headless()
    #     driver = webdriver.Chrome(executable_path='D:/360极速浏览器下载/chromedriver.exe')
    #
    #     driver.get(login_url)
    #
    #     # 向浏览器发送用户名、密码，并点击登录按钮
    #     driver.find_element_by_name('u').send_keys(self.username)
    #     driver.find_element_by_name('p').send_keys(self.passwd)
    #     response = driver.find_element_by_css_selector('.simple + button').submit()
    #     # response = driver.find_element("css selector","form>button[type='submit']")
    #     print('-->response')
    #     print('submited...')
    #
    #     s = requests.Session()
    #     cookies = driver.get_cookies()
    #     print('-->cookies',cookies)
    #     for cookie in cookies:
    #         s.cookies.set(cookie['name'],cookie['value'])
    #     driver.close()
    #
    #     page_url = 'http://share.blizzmi.local/dokuwiki/doku.php?id=start&do=admin&page=usermanager'
    #     resp = s.get(page_url)
    #     resp.encoding = 'utf-8'
    #     print('status_code = {0}'.format(resp.status_code))
    #     print('status_code',resp.text)

    def add_doku(self,pro):
        data = {"do": "login", "id": "start", "p": "6520sl", "sectok": "", "u": "admin"}
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        s = requests.session()
        login = s.post("http://share.blizzmi.local/dokuwiki/doku.php?id=start",data = data,headers = header)
        # print('-->login.text',login.text)
        tok = re.search("sectok=(.*)\"\s.*class",login.text).group(1)
        print('tok',tok)
        login_url = "http://share.blizzmi.local/dokuwiki/doku.php?id=start"
        # opt = webdriver.ChromeOptions()
        # # opt.set_headless()
        # driver = webdriver.Chrome(executable_path='D:/360极速浏览器下载/chromedriver.exe')
        #
        # driver.get(login_url)
        #
        # # 向浏览器发送用户名、密码，并点击登录按钮
        # driver.find_element_by_name('u').send_keys('admin')
        # driver.find_element_by_name('p').send_keys('6520sl')
        # response = driver.find_element_by_css_selector('.simple + button').submit()
        # # response = driver.find_element("css selector","form>button[type='submit']")
        # print('-->response')
        # print('submited...')

        # s = requests.Session()
        # cookies = driver.get_cookies()
        # print('-->cookies',cookies)
        # for cookie in cookies:
        #     s.cookies.set(cookie['name'],cookie['value'])
        # # driver.close()
        #
        # page_url = 'http://share.blizzmi.local/dokuwiki/doku.php?id=start&do=admin&page=usermanager'
        # resp = s.get(page_url)


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
        regdoku = s.post("http://share.blizzmi.local/dokuwiki/doku.php?id=start", data=regdata, headers=header)
        # print('regdoku', regdoku.text)

        tok2 = re.search("sectok=(.*)\"\s.*class",regdoku.text).group(1)
        print('tok2',tok2)
        # # driver.get(page_url)
        # x = driver.find_elements_by_css_selector('input[type=checkbox][name="delete[zhaogr]"]')
        # print('-->x',x)
        # x[0].click()
        deldata = {
            "sectok": tok,
            "userid": self.username,
            "username": self.realname,
            "usermail": self.email,
            "usergroups": 'user,' + pro,
            "fn[delete]": '',
            "delete[%s]" % self.username: 'on',
            "do": 'admin',
            "page": 'usermanager',
            "start": '0',
            "filter[user]": self.username,
            # "fn[search][new]":'',
        }


        # xxxdoku = s.post("http://share.blizzmi.local/dokuwiki/doku.php?id=start", data=deldata, headers=header)
        # print('xxxdoku',xxxdoku.text)
        # xxxdoku.status_code

    def del_doku(self,pro):
        print('\033[;34m删除doku账户\033[0m')
        data = {"do": "login", "id": "start", "p": "6520sl", "sectok": "", "u": "admin"}
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        s = requests.session()
        login = s.post("http://share.blizzmi.local/dokuwiki/doku.php?id=start",data = data,headers = header)
        tok = re.search("sectok=(.*)\"\s.*class",login.text).group(1)
        print('tok',tok)

        deldata = {
            "sectok": tok,
            "userid": self.username,
            "username": self.realname,
            "usermail": self.email,
            "usergroups": 'user,' + pro,
            "fn[delete]": '',
            "delete[%s]" % self.username: 'on',
            "do": 'admin',
            "page": 'usermanager',
            "start": '0',
            "filter[user]": self.username,
            # "fn[search][new]":'',
        }


        deldoku = s.post("http://share.blizzmi.local/dokuwiki/doku.php?id=start", data=deldata, headers=header)
        print('-->deldoku',deldoku.status_code)

    # def add_doku(self, pro):
    #     data = {"do": "login", "id": "start", "p": "6520sl", "sectok": "", "u": "admin"}
    #     header = {"Content-Type": "application/x-www-form-urlencoded"}
    #     s = requests.session()
    #     login = s.post("http://share.blizzmi.local/dokuwiki/doku.php?id=start", data=data, headers=header)
    #     # print('-->login.text',login.text)
    #     tok = re.search("sectok=(.*)\"\s.*class", login.text).group(1)
    #     print('tok', tok)
    #
    #     login_url = "http://share.blizzmi.local/dokuwiki/doku.php?id=start"
    #     # opt = webdriver.ChromeOptions()
    #     # opt.set_headless()
    #     driver = webdriver.Chrome(executable_path='D:/360极速浏览器下载/chromedriver.exe')
    #
    #     driver.get(login_url)
    #
    #     # 向浏览器发送用户名、密码，并点击登录按钮
    #     driver.find_element_by_name('u').send_keys(self.username)
    #     driver.find_element_by_name('p').send_keys(self.passwd)
    #     response = driver.find_element_by_css_selector('.simple + button').submit()
    #     # response = driver.find_element("css selector","form>button[type='submit']")
    #     print('-->response')
    #     print('submited...')
    #
    #     s = requests.Session()
    #     cookies = driver.get_cookies()
    #     print('-->cookies',cookies)
    #     for cookie in cookies:
    #         s.cookies.set(cookie['name'],cookie['value'])
    #     driver.close()
    #
    #     page_url = 'http://share.blizzmi.local/dokuwiki/doku.php?id=start&do=admin&page=usermanager'
    #     resp = s.get(page_url)
    #     resp.encoding = 'utf-8'
    #     print('status_code = {0}'.format(resp.status_code))
    #     print('status_code',resp.text)

    def del_jira(self):
        print('\033[;34m删除jira账户\033[0m')
        response_dict = {'name':'jira','status':True,'error':None,'data':None}
        x = JIRA('http://jira.blizzmi.local/', basic_auth=('sunsw', 'b4b1a6'))
        try:
            # x.user(self.username)
            exists_user = x.search_users(self.username)
            if exists_user:
                if '离职' in exists_user[0].displayName:
                    response_dict['status'] = False
                    response_dict['error'] = '账号已删除,不要重复操作'
                    return response_dict
                for group in x.groups():
                    if self.username in x.group_members(group):
                        print(group)
                        # response_dict['data'].append(group)
                        x.remove_user_from_group(self.username, group)
                    # else:
                    #     response_dict['status'] = False
                    #     response_dict['error'] = 'jira用户不存在'
                x.user(self.username).update(displayName='%s_【离职】' % self.realname)
                # x.rename_user(self.username, '%s_dimission' % self.username)
                response_dict['data'] = 'jira账号已删除'
            else:
                response_dict['status'] = False
                response_dict['error'] = '账号不存在'

        except JIRAError as e:
            response_dict['status'] = False
            response_dict['error'] = e.text
        return response_dict

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
