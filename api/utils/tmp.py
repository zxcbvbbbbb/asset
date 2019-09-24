import requests
from subprocess import *


def exec_cmd(cmd):
    res = Popen(cmd, shell=True, stdout=PIPE)
    ret = res.communicate()[0].decode('utf-8')
    return ret.strip()

cmd = "curl https://dnsapi.cn/Domain.List -d 'login_token=111640,939779be5e82635b8a63e21150628da5&format=json'"
exec_cmd(cmd)