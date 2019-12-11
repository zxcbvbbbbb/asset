#!/bin/python
# -*- coding:utf-8 -*-

import string,random,sys,pexpect
from subprocess import *

def manual_input(cmd):
    child = pexpect.spawn(cmd)
    child.expect(':')
    child.sendline('')
    print(child.before)
    child.expect(':')
    child.sendline('123')
    child.expect(':')
    child.sendline('123')

def exec_cmd(cmd):
    call(cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr)

user_list = ['simon','tongfei','hejh','hesd','hezq','hegp','heziq','hert','yuxin','fengly','liuyun','liuting','liulk','liufr','liuyl','baorj','xiangzh','lvmin','wugx','wuss','zhouxj','zhoubs','xiadf','jiangqian','sunsw','sunym','ninggq','anwei','songhb','songxiang','yinzy','yuekui','zhuangtt','liaonh','liaowc','liaowh','liaoxin','zhangyl','zhanglh','zhanghl','zhangqm','zhangyj','zhangzx','zhangfc','zhangzan','zhangzhen','jeemin','geqin','davymai','daisj','zengyong','zengdz','zenghui','zenghs','zhubb','liqq','liyong','lihy','lixin','lihb1','lihc','limeng','yangcc','yangyp','lianggs','liangrx','liangliang','liangsk','ouxr','ouhj','ouyanggf','tangrb','honggh','panll','panjs','niuhl','wangzj','wangjj','wangxb','ganjx','huyu','rongxia','morf','caicj','zhanjg','shenzl','xiebiao','tanyw','tanzx','heyc','dengsl','dengym','denglh','zhongbao','zhonggn','ruansx','chenli','chengm','chenbq','chenjl','chenxl','chenhaiy','hanxl','raolj','majin','masong','luming','huangwu','huangjl','huangxing','huangzh','huangzb','huangyao','huangjx']
test_list = ['hert','yuxin']

for item in test_list:
    random_list = random.sample((string.ascii_lowercase+string.digits),8)
    pwd = ''.join(random_list)
    cmd1 = 'useradd %s' % item
    cmd2 = 'smbpasswd -a %s' % item
    manual_input(cmd2)
    cmd3 = 'mkdir /data/smb/{0};chown {0}.{0} /data/smb/{0}'.format(item)
    exec_cmd(cmd1)
    exec_cmd(cmd2)
    print('用户名：'+item+'\n'+'密码'+pwd)
    exec_cmd(cmd3)

# user_list = ['simon','tongfei','hejh','hesd','hezq','hegp','heziq','hert','yuxin','fengly','liuyun','liuting','liulk','liufr','liuyl','baorj','xiangzh','lvmin','wugx','wuss','zhouxj','zhoubs','xiadf','jiangqian','sunsw','sunym','ninggq','anwei','songhb','songxiang','yinzy','yuekui','zhuangtt','liaonh','liaowc','liaowh','liaoxin','zhangyl','zhanglh','zhanghl','zhangqm','zhangyj','zhangzx','zhangfc','zhangzan','zhangzhen','jeemin','geqin','davymai','daisj','zengyong','zengdz','zenghui','zenghs','zhubb','liqq','liyong','lihy','lixin','lihb1','lihc','limeng','yangcc','yangyp','lianggs','liangrx','liangliang','liangsk','ouxr','ouhj','ouyanggf','tangrb','honggh','panll','panjs','niuhl','wangzj','wangjj','wangxb','ganjx','huyu','rongxia','morf','caicj','zhanjg','shenzl','xiebiao','tanyw','tanzx','heyc','dengsl','dengym','denglh','zhongbao','zhonggn','ruansx','chenli','chengm','chenbq','chenjl','chenxl','chenhaiy','hanxl','raolj','majin','masong','luming','huangwu','huangjl','huangxing','huangzh','huangzb','huangyao','huangjx']
# for item in user_list:
#     exec_cmd('userdel -r {0}'.format(item))
