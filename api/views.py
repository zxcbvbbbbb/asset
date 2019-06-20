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
from selenium import webdriver
from jira import JIRA
from jira.exceptions import JIRAError
import requests


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
                return redirect('/index')
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
        current_page = request.GET.get('p')
        current_page = int(current_page)
        start_page = (current_page -1) * 10
        end_page = current_page * 10
        classes = models.Classes.objects.all()[start_page:end_page]
        username = request.session.get('username')
        total_count = models.Classes.objects.all().count()
        v, a = divmod(total_count, 10)
        pager_list = []
        pager_list.append('<a href="/classes/?p=%s">上一页</a>' % (current_page - 1))
        page_range_start = current_page - 5
        page_range_end = current_page + 5 + 1
        for i in range(page_range_start, page_range_end):
            if i == current_page:
                pager_list.append('<a class="active" href="/classes/?p=%s">%s</a>' % (i, i))
            else:
                pager_list.append('<a href="/classes/?p=%s">%s</a>' % (i, i))
        pager_list.append('<a href="/classes/?p=%s">下一页</a>' % (current_page + 1))
        str_pager = ''.join(pager_list)
        return render(request,'classes.html',{'username':username,'classes':classes,'str_pager':str_pager})
    elif request.method == 'POST':
        caption = request.POST.get('caption')
        response_dict = {'status':True,'error':None,'data':None}
        if caption:
            c = models.Classes.objects.filter(caption=caption).count()
            if not c:
                models.Classes.objects.create(caption=caption)
                for i in range(500):
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
def handle_student(request):

    username = request.session.get('username')
    return render(request,'student.html',{'username':username})

@auth
def handle_teacher(request):

    username = request.session.get('username')
    return render(request,'teacher.html',{'username':username})


def modal(request):
    print(request.GET.get('p'))
    driver = webdriver.Chrome(executable_path='D:/360极速浏览器下载/chromedriver.exe')
    driver.get('D:/posttest/templates/doku2.html')
    # s = driver.find_elements_by_css_selector('input[type=checkbox][name="delete[zhaogr]"]')
    # s[0].click()
    s = driver.find_element_by_css_selector('[type=submit]')
    print('-->s',s)
    return render(request,'modal.html')

def addnew(request):
    if request.method == 'POST':
        realname = request.POST['realname']
        pro = request.POST['pro']
        job = request.POST['job']
        new = reg.register(realname,job)
        # new.sendbc(pro)
        # statjira = new.add_jira()
        # if statjira == False:
        #     return HttpResponse("请勿重复注册！")
        username = new.username
        passwd = new.passwd
        name = new.realname
        if job in ("测试","开发","PO","运维"):
            # new.del_mantis()
            new.add_jira()
            # new.add_mantis()
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

def dropuser(request):
    if request.method == 'POST':
        realname = request.POST['realname']
        # if not check_name(realname):
        #     return HttpResponse(10000)
        new = reg.register(realname, 70)
        username = new.username
        passwd = new.passwd
        name = new.realname
        rep_jira = new.del_jira()
        print('-->rep_jira', rep_jira)
        if rep_jira['status']:
            rep_mantis = new.del_mantis()
            rep = {'jira':rep_jira,'mantis':rep_mantis}
            return JsonResponse(rep)
        # rep = {'jira':rep_jira,'mantis':{'name':'mantis','status':False,'error':'请先删除jira账号'}}
        rep = {'jira': rep_jira}
        print('-->rep',rep)
        return JsonResponse(rep)

    elif request.method == 'GET':
        return render(request, 'register/dropuser.html',{"hidden": "hidden"})















