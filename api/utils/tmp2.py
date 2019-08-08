from subprocess import Popen,PIPE
import json,os

def exec_cmd(cmd):
    res = Popen(cmd,shell=True,stdout=PIPE)
    ret = res.communicate()[0].decode('utf-8')
    return ret

cmd = 'curl -H "X-Consul-Token: blizzmi.us007" -s -G http://192.168.200.60:8500/v1/agent/services|json'
services = exec_cmd(cmd)
data = []
for item in json.loads(services):
    data.append({'title':item})

newdata = 'var data1 = %s' % data
print(newdata)
from s7day129 import settings
filename = os.path.join(settings.BASE_DIR,'static\js\data.js')
print(filename)
with open(filename,'w',encoding='utf-8') as f:
    f.write(newdata)