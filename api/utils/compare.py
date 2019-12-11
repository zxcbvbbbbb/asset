from jira import JIRA
from jira.exceptions import JIRAError
import requests,pymysql
import os
from s7day129 import settings


x = JIRA('https://jira.99808.net', basic_auth=('sunsw', 'b4b1a6'))

def get_bcusers():
    getUrl = 'https://api.bearychat.com/v1/user.list?token=049ecceaea09856c86236fef0068c8d6'
    info = requests.get(getUrl).json()
    name_list = [ item['name'] for item in info ]
    fullname_list = [ item['full_name'] for item in info ]

    name_list.extend(set(fullname_list))
    return name_list

def get_jirausers():
    print('\033[;34m比较jira账号\033[0m')
    y = dict(x.group_members('jira-software-users'))
    users = []
    for xxx in y.items():
        users.append(xxx[1]['fullname'])
    return users

def get_dokuusers():
    print('\033[;34m比较doku账号\033[0m')
    file_path = os.path.join(settings.BASE_DIR,'static','wikiusers.csv')
    f = open(file_path, 'r', encoding='utf-8')
    user_list = []
    for line in f.readlines():
        line = line.split(',')
        user_list.append(line[1])

    f.close()
    user_list.pop(0)
    return user_list

def get_mantisusers():
    print('\033[;34m比较mantis账号\033[0m')
    user_list = []
    try:
        db = pymysql.connect("127.0.0.1","mantis","ZroXnQDlcJs7lgJ6", \
                             "mantis", use_unicode=True, charset="utf8mb4")
        cursor = db.cursor()
        sql = "SELECT realname FROM mantis_user_table"
        cursor.execute(sql)
        data = cursor.fetchall()
        for row in data:
            user_list.append(row[0])
        db.close()
        return user_list

    except pymysql.err.OperationalError as e:
        print(e)

def account_compare():
    account = {}
    bcusers = set(get_bcusers())
    founded_jira = set(get_jirausers()) - bcusers
    print(founded_jira)
    account['jira'] = list(founded_jira)
    founded_doku = set(get_dokuusers()) - bcusers
    print(founded_doku)
    account['doku'] = list(founded_doku)
    founded_mantis = set(get_mantisusers()) - bcusers
    if founded_mantis:
        print(founded_mantis)
        account['mantis'] = list(founded_mantis)
    else:
        print('ok')
    return account

