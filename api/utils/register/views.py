from django.shortcuts import render
from django.http import HttpResponse
from ops.zabbix import Zbx
from ops.salt import Salt
import ops.allEnvGames
import ops.compMd5
import json
from ops import reg
# Create your views here.
def zbxitems(request):
    zbx = Zbx()
    groups = zbx.getgroups()
    if request.method == "POST":
        groupid = request.POST['groups']
        hostid = request.POST['hosts']
        items = zbx.getitems(hostid)
        groupname = groups[groupid] + "："
        hostname = zbx.gethosts(groupid)[hostid]
        return render(request, 'ops/zbx.html',{'groups': groups,'items': items,'groupname':groupname,'hostname':hostname})
    else:
        hidden="hidden"
        return render(request, 'ops/zbx.html',{'groups': groups,"hidden": hidden})
def zbxhost(request):
    zbx = Zbx()
    pk = request.GET['pk']
    hosts = zbx.gethosts(pk)
    return HttpResponse(json.dumps(hosts))

#def zbxittb(request):
#    pk2 = request.GET['pk2']
#    items = zbx.getitems(pk2)
#    return HttpResponse(json.dumps(items))
#    return render(request, 'ops/items.html',{'items': items})
def saltfun(request):
    st = Salt()
    st.login()
    keyHostsList = st.getKeyHosts()
    modsList = st.getFunctions().keys()
    hidden = "hidden"
    if request.method == "POST":
        hosts = request.POST['hosts']
        if hosts == "请选择":
            statusHosts = st.getStatusHosts()
            return render(request, 'ops/salt.html',{'keyHostsList': keyHostsList,'modsList': modsList,'statusHosts':statusHosts})
        mods = request.POST['mods']
        funs = request.POST['funs']
        arg = request.POST['arg']
        command = 'salt "{}" {}.{} "{}"'.format(hosts,mods,funs,arg)
        result = st.runFun(tgt=hosts, fun="{}.{}".format(mods,funs), arg=arg)
#        return HttpResponse(json.dumps(result))
        return render(request, 'ops/salt.html',{'keyHostsList': keyHostsList,'modsList': modsList,'result': result,"hidden": hidden,"command": command})
    else:
        return render(request, 'ops/salt.html',{'keyHostsList': keyHostsList,'modsList': modsList,"hidden": hidden})
def saltmods(request):
    st = Salt()
    st.login()
    pk = request.GET['pk']
    funsList = st.getFunctions()[pk]
    return HttpResponse(json.dumps(funsList))

def gameinfo(request):
    envall = ops.allEnvGames.all_run()
    return render(request, 'ops/gameinfo.html',{'envall': envall})

def getmd5(request):
    md5all = {}
    if request.method == "POST":
        env1 = request.POST['env1']
        env2 = request.POST['env2']
        game_type = request.POST['game_type']
        game_id = request.POST['game_id']
        md5all = ops.compMd5.all_run(env1,env2,game_type,game_id)
        for v in md5all.values():
            v[1]['env1'] = v[1].pop(env1)
            v[1]['env2'] = v[1].pop(env2)
        return render(request, 'ops/md5sum.html',{'env1': env1,'env2': env2,'game_type':game_type,'game_id':game_id,'md5all': md5all})
    else:
        hidden = "hidden"
        return render(request, 'ops/md5sum.html',{"hidden": hidden})
def addnew(request):
    if request.method == 'POST':
        realname = request.POST['realname']
        pro = request.POST['pro']
        job = request.POST['job']
        new = reg.register(realname,job)
        new.sendbc(pro)
        statjira = new.add_jira()
        if statjira == False:
            return HttpResponse("请勿重复注册！")
        username = new.username
        passwd = new.passwd
        name = new.realname
        if job in ("测试","开发","PO","运维"):
            new.add_mantis()
            new.add_doku(pro)
            return render(request, 'ops/reg.html',{"username": username,"passwd": passwd,"name":name})
        else:
            return render(request, 'ops/reg.html',{"username": username,"passwd": passwd,"hidden2": "hidden","name":name})
    else:
        return render(request, 'ops/reg.html',{"hidden": "hidden"})
