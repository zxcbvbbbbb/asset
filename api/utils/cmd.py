from subprocess import *

def exec_cmd(cmd):
    res = Popen(cmd, shell=True, stdout=PIPE)
    ret = res.communicate()[0].decode('utf-8')
    return ret.strip()