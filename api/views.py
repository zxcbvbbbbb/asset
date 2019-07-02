from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication
from api.utils.permission import SVIPPermission
from api.utils.permission import MyPermission1
from api.utils.throttle import VisitThrottle
from api import models
from django.views.generic.edit import CreateView
from .forms import ClientForm
from .models import Client,City,UserInfo
import json
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.views import View
from django.http.request import QueryDict
from api.utils.register import reg
from jira import JIRA
from jira.exceptions import JIRAError
import requests,os,re
from api.utils.cmd import exec_cmd
from api.utils.compare import account_compare


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    # templame_name = 'client_form1.html'
    template_name = 'client_form.html'

def ajax_load_cities(request):
    if request.method == 'GET':
        country_id = request.GET.get('country_id')
        if country_id:
            data = list(City.objects.filter(country_id=country_id).values('id','name'))
            print('-------->data',data)
            return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


def posttest(request):
    print(request)
    if request.method == 'POST':
        print(request.POST)
    return render(request,'posttest.html')

class Test(APIView):
    def post(self,request,*args,**kwargs):
        name = request.data['username']
        passwd = request.data['password']
        user = authenticate(username=name,password=passwd)
        try:
            user = models.UserInfo.objects.get(name=name)
            pwd = user.password
            if check_password(passwd,pwd): #验证明文密码
                if user.is_active:
                    print('-->request.user',request.user)
                    login(request,user)
                    print('-->request._request', request._request.COOKIES)
                    print('user %s is login' % user,request.user)
                    # logout(request)
                    # print('user %s is logout' % user, request.user)
                else:
                    print('no such user')
            else:
                return JsonResponse({'error':'密码错误'})
            ret = {'code':2000,'token':'admin'}
            return JsonResponse(ret,status=201)
        except UserInfo.DoesNotExist:
            return JsonResponse({'code':20001,'error':'user does not exist.'},status=202)

# def login(request):
#     msg = ''
#     v = request.session
#     if request.method == 'POST':
#         user = request.POST.get('username')
#         pwd = request.POST.get('password')
#
#         obj = UserInfo.objects.filter(name=user).first()
#         if not obj:
#             msg = '用户不存在'
#             return render(request,'login.html',{'msg':msg})
#         if  check_password(pwd,obj.password):
#             request.session['is_login'] = True
#             request.session['username'] = user
#             return redirect('/index')
#         else:
#             msg = '登录失败'
#             # return render(request,'login.html',{'msg':msg})
#     return render(request,'login.html',{'msg':msg})

class Login(APIView):
    def get(self,request,*args,**kwargs):
        return render(request,'login.html',{'msg':''})
    def post(self,request,*args,**kwargs):
        msg = ''
        user = request.data['username']
        pwd = request.data['password']
        try:
            obj = models.UserInfo.objects.get(name=user)
            if check_password(pwd, obj.password):
                request._request.session['is_login'] = True
                request._request.session['username'] = user
                print('-->check password',request._request.session['is_login'])
                return redirect('/')
            else:
                msg = '密码错误'
                return render(request, 'login.html', {'msg': msg})
        except UserInfo.DoesNotExist:
            msg = 'user does not exist.'
            return render(request, 'login.html', {'msg': msg})


def logout(request):
    request.session.clear()
    return redirect('/login')

def auth(func):
    def inner(request,*args,**kwargs):
        is_login = request.session.get('is_login')
        print('-->is_login',is_login)
        if is_login:
            return func(request,*args,**kwargs)
        else:
            return redirect('/login')
    return inner

@auth
def index(request):
    current_user = request.session.get('username')
    print('-->current_user',current_user)
    return render(request,'index.html',{'username':current_user})

@auth
def handle_classes(request):
    if request.method == 'GET':
        # 当前页
        current_page = request.GET.get('p',1)
        current_page = int(current_page)

        # 所有数据的个数
        total_count = models.Classes.objects.all().count()

        from api.utils.page import PagerHelper
        obj = PagerHelper(total_count, current_page, '/classes',5)
        pager = obj.pager_str()

        cls_list = models.Classes.objects.all()[obj.db_start:obj.db_end]

        current_user = request.session.get('username')
        return render(request,'classes.html',{'username':current_user,'classes':cls_list,'str_pager':pager})
    elif request.method == 'POST':
        caption = request.POST.get('caption')
        response_dict = {'status':True,'error':None,'data':None}
        if caption:
            c = models.Classes.objects.filter(caption=caption).count()
            if not c:
                models.Classes.objects.create(caption=caption)
                for i in range(50):
                    models.Classes.objects.create(caption=caption+str(i))
                response_dict['data'] = '添加成功'
            else:
                response_dict['status'] = False
                response_dict['error'] = '班级已存在'
        else:
            response_dict['status'] = False
            response_dict['error'] = '班级名不能为空'
        print('-->response_dict',response_dict)
        return JsonResponse(response_dict)

@auth
def edit_class(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        obj = models.Classes.objects.filter(id=nid).first()
        return render(request,'edit_class.html',{'obj':obj})
    elif request.method == 'POST':
        nid = request.POST.get('nid')
        caption = request.POST.get('caption')
        models.Classes.objects.filter(id=nid).update(caption=caption)
        return redirect('/classes')
    else:
        return redirect('/')

@auth
def handle_student(request):
    if request.method == 'GET':
        user = request.session.get('username')
        return render(request, 'student.html',{'username':user})
    elif request.method == 'POST':
        name = request.POST.get('name')
        exec_cmd(
            'curl -X PUT -s --header "X-Consul-Token: blizzmi.us007" http://192.168.200.60:8500/v1/agent/service/deregister/%s' % name)
        headers = {"X-Consul-Token": "blizzmi.us007"}
        r = requests.get('http://192.168.200.60:8500/v1/agent/service/%s' % name,
                         )
        print('-->code', r.status_code)
        response_dict = {'status': True, 'msg': None}
        if r.status_code == 404:
            response_dict['msg'] = '删除成功！'
            return JsonResponse(response_dict)
        else:
            response_dict['status'] = False
            response_dict['msg'] = r.text
            return JsonResponse(response_dict)

@auth
def handle_teacher(request):

    username = request.session.get('username')
    teacher_list = models.Teacher.objects.filter(id__in=models.Teacher.objects.all()).values('id','name','cls__id','cls__caption')
    result = {}
    cls_list = []
    for t in teacher_list:
        if t['id'] in result:
            if t['cls__id'] != 'None':
                cls_list.append({'id':t['cls__id'],'caption':t['cls__caption']})
                print('-->cls_list',cls_list)
        else:
            cls_list = [{'id':t['cls__id'],'caption':t['cls__caption']}]
        result[t['id']] = {'nid':t['id'],'name':t['name'], 'cls_list':cls_list}
    print(result)
    return render(request,'teacher.html',{'username':username,'teachers':result})

@auth
def add_teacher(request):
    if request.method == 'GET':
        cls_list = models.Classes.objects.all()
        return render(request,'add_teacher.html',{'cls_list':cls_list})
    elif request.method == 'POST':
        teacher = request.POST.get('teacher')
        cls = request.POST.getlist('cls')
        print('-->cls',cls)
        obj = models.Teacher.objects.create(name=teacher)
        obj.cls.add(*cls)
        return redirect('/teacher')

@auth
def edit_teacher(request,nid):
    if request.method == 'GET':
        obj = models.Teacher.objects.get(id=nid)
        obj_cls_list = obj.cls.all().values_list('id','caption')
        print(bool(obj_cls_list))
        id_list = list(zip(*obj_cls_list))[0] if obj_cls_list else []
        print('-->id_list',id_list)
        cls_list = models.Classes.objects.exclude(id__in=id_list)
        print('-->cls_list',cls_list)
        return render(request, 'edit_teacher.html',{'obj':obj,'id_list':id_list,'cls_list':obj_cls_list,'exclude_list':cls_list})
    elif request.method == 'POST':
        name = request.POST.get('name')
        cls_li = request.POST.getlist('cls')
        print('-->cls_li',cls_li)
        obj = models.Teacher.objects.get(id=nid)
        obj.name = name
        obj.save()
        obj.cls.set(cls_li)
        return redirect('/teacher/')

def modal(request):
    print(request.GET.get('p'))
    driver = webdriver.Chrome(executable_path='D:/360极速浏览器下载/chromedriver.exe')
    driver.get('D:/posttest/templates/doku2.html')
    # s = driver.find_elements_by_css_selector('input[type=checkbox][name="delete[zhaogr]"]')
    # s[0].click()
    s = driver.find_element_by_css_selector('[type=submit]')
    print('-->s',s)
    return render(request,'modal.html')

@auth
def addnew(request):
    if request.method == 'POST':
        realname = request.POST['realname']
        pro = request.POST['pro']
        job = request.POST['job']
        new = reg.register(realname,job)
        # new.sendbc(pro)
        statjira = new.add_jira()
        # if statjira == False:
        #     return HttpResponse("请勿重复注册！")
        username = new.username
        passwd = new.passwd
        name = new.realname
        if job in ("测试","开发","PO","运维"):
            # new.add_jira()
            new.add_mantis()
            # new.add_doku(pro)
            return render(request, 'register/reg.html',{"username": username,"passwd": passwd,"name":name})
        else:
            return render(request, 'register/reg.html',{"username": username,"passwd": passwd,"hidden2": "hidden","name":name})
    else:
        return render(request, 'register/reg.html',{"hidden": "hidden"})

def check_name(name):
    getUrl = 'https://api.bearychat.com/v1/user.list?token=049ecceaea09856c86236fef0068c8d6'
    req_info = requests.get(getUrl).json()
    for i in req_info:
        if (i['name'] == name or i['full_name'] == name) and i['inactive'] == False:
            return True
@auth
def dropuser(request):
    if request.method == 'POST':
        realname = request.POST['realname']
        if not check_name(realname):
            return HttpResponse(10000)
        new = reg.register(realname, 70)
        username = new.username
        passwd = new.passwd
        name = new.realname
        rep_jira = new.del_jira()
        print('-->rep_jira', rep_jira)
        rep = {'jira': rep_jira}
        if rep_jira['status']:
            rep_mantis = new.del_mantis()
            rep.update({'mantis': rep_mantis})
            if rep_mantis['status']:
                rep_doku = new.del_doku()
                rep.update({'doku':rep_doku})
            # rep = {'jira':rep_jira,'mantis':rep_mantis}
            return JsonResponse(rep)
        print('-->rep', rep)
        return JsonResponse(rep)

    elif request.method == 'GET':
        user = request.session.get('username')
        return render(request, 'register/dropuser.html',{"hidden": "hidden",'username':user})

def upload(request):
    if request.method == 'GET':
        img_list = models.Img.objects.all()
        print(img_list)
        return render(request,'upload.html',{'images':img_list})
    elif request.method == 'POST':
        obj = request.FILES.get('tftp')
        file_path = os.path.join('static','upload',obj.name)
        f = open(file_path,'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()
        models.Img.objects.create(path=file_path)
        return redirect('/upload')

def search(request):
    if request.method == 'GET':
        q = request.GET.get('q')
        print(q)
        objs = models.Classes.objects.filter(caption__contains=q)
        l = [ obj.caption for obj in objs ]
        print(l)

        return JsonResponse(l,safe=False)

@auth
def test(request):
    user = request.session.get('username')
    service = {}
    if request.method == 'GET':
        return render(request,'test.html',{'username':user})
    elif request.method == 'POST':
        name = request.POST.get('name')
        type = request.POST.get('type')
        tags = request.POST.get('tags')
        address = request.POST.get('address')
        port = request.POST.get('port')
        print('-->type', type)
        print('-->tags',tags)
        print('-->address', address)
        print('-->port',port)
        service['Name'] = name
        service['Tags'] = re.split('[,， ]',tags)
        service['Tags'].append('正式玩')
        print(service['Tags'])
        service['Address'] = address
        service['Port'] = int(port)
        service["ID"] = "prod_%s_%s_%s" % (type, address,port)
        test = {'Name': 'test', 'Tags': ['ws_exporter', 'xx', 'yy', '正式玩'], 'Address': 'a.bc.com', 'Port': 443,
                'ID': 'prod_swf_swf.fgfg0606.com_443'}
        headers = {"X-Consul-Token": "blizzmi.us007"}
        print(service)
        r = requests.put('http://192.168.200.60:8500/v1/agent/service/register', json=service,headers=headers)
        if r.status_code != 200:
            return JsonResponse({'msg':r.text})
        return JsonResponse({'msg':'添加成功'})

@auth
def compare(request):
    if request.method == 'GET':
        user = request.session.get('username')
        accounts = account_compare()
        print('-->accounts',accounts)
        return render(request, 'compare.html',{'accounts':accounts,'username':user})











