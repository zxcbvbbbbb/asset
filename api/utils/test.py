from jira import JIRA
from jira.exceptions import JIRAError
import requests,pymysql


x = JIRA('http://jira.blizzmi.local/', basic_auth=('sunsw', 'b4b1a6'))

def get_bcusers():
    getUrl = 'https://api.bearychat.com/v1/user.list?token=049ecceaea09856c86236fef0068c8d6'
    info = requests.get(getUrl).json()
    name_list = [ item['name'] for item in info ]
    fullname_list = [ item['full_name'] for item in info ]

    name_list.extend(set(fullname_list))
    return name_list

def get_jirausers():
    y = dict(x.group_members('jira-software-users'))
    users = []
    for xxx in y.items():
        users.append(xxx[1]['fullname'])
    return users

def get_dokuusers():
    f = open('wikiusers.csv', 'r', encoding='utf-8')
    user_list = []
    for line in f.readlines():
        line = line.split(',')
        user_list.append(line[1])

    f.close()
    user_list.pop(0)
    return user_list

def get_mantisusers():
    user_list = []
    try:
        db = pymysql.connect("192.168.200.150","mantis","ZroXnQDlcJs7lgJ6", \
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


founded_jira = set(get_jirausers()) - set(get_bcusers())
founded_doku = set(get_dokuusers()) - set(get_bcusers())
founded_mantis = set(get_mantisusers()) - set(get_bcusers())
print('jira账号:   {0}'.format(founded_jira))
print('doku账号:   {0}'.format(founded_doku))
print('mantis账号: {0}'.format(founded_mantis))



