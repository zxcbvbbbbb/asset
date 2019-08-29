#!/usr/bin/python

from subprocess import *
import json,time
from datetime import datetime

#镜像示例
#https://reg.blizzmi.net/api/projects      查看project_id
#https://reg.blizzmi.net/api/repositories/douyu/dao_serve/tags       获取douyu仓库下的所有镜像
#https://reg.blizzmi.net/api/repositories/douyu/dao_serve/tags/dev_a8662423     douyu仓库下的单个镜像
#curl -X DELETE -H 'Accept: text/plain' -u admin:blizzmi.US007 https://reg.blizzmi.net//api/repositories/douyu/dao_serve/tags/dev_0651c3de      删除单个镜像
#curl -s -X GET --header 'Accept: application/json' https://reg.blizzmi.net//api/repositories/douyu/dao_serve/tags | grep \"name\"|awk -F '"' '{print $4}'|sort -r |awk 'NR > 9 {print $1}'    获取douyu仓库下的所有镜像标签

def exec_cmd(cmd):
    res = Popen(cmd ,shell=True ,stdout=PIPE)
    ret = res.communicate()[0]
    return ret.strip()

URL="https://reg.blizzmi.net"
PRO="douyu"
USER="admin"
PASS="blizzmi.US007"
project_id = 5 #douyu的project_id

#通过projects_id获取repositories,这里是获取douyu项目下的镜像仓库['agent_api_serve', 'api_server', 'dao_serve', 'dy_admin', 'task_worker']
REPOS = json.loads(exec_cmd("curl -s -X GET --header 'Accept: application/json' %s/api/repositories?project_id=%s" % (URL,project_id)))
repo_list = []
for item in REPOS:
    repo_list.append(item['name'].split('/')[1])
print(repo_list)


def del_tags(repo,data):
    tag_dict = {}
    current_time = datetime.now()
    for item in data:
        if item['digest']:
            digest = item['digest'][7:]
            created = item['created'][:10]
            t = time.strptime(created, '%Y-%m-%d')
            limit_days = (current_time - datetime(t.tm_year, t.tm_mon, t.tm_mday)).days
            if limit_days < 1:
                continue
            print('-->limit_days', limit_days)
            if digest in tag_dict:
                tag_dict[digest].append(item['name'])
            else:
                tag_dict[digest] = item['name'].split()

    print('-->tag_dict',tag_dict)

    #删除一个月前的
    for item in tag_dict.values():
        if len(item) == 1:
            print('软删除 %s %s' % (repo,item[0]))
            exec_cmd("curl -s -X DELETE -H 'Accept: text/plain' -u %s:%s %s/api/repositories/%s/%s/tags/%s" % (USER,PASS,URL,PRO,repo,item[0]))

for repo in repo_list:
    data = json.loads(exec_cmd("curl -s -X GET --header 'Accept: application/json' %s/api/repositories/%s/%s/tags" % (URL,PRO,repo)))
    del_tags(repo,data)
