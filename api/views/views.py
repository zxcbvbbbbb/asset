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
from api.forms import ClientForm
from api.models import Client,City,UserInfo
import json
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.views import View
from django.http.request import QueryDict
from api.utils.register import reg
from jira import JIRA
from jira.exceptions import JIRAError
import requests,os,re,hashlib
from api.utils.cmd import exec_cmd
from api.utils.compare import account_compare
from django.forms import fields
from django import forms

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
    return render(request, 'posttest.html')

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

# class Login(APIView):
#     def get(self,request,*args,**kwargs):
#         return render(request,'login.html',{'msg':''})
#     def post(self,request,*args,**kwargs):
#         msg = ''
#         user = request.data['username']
#         pwd = request.data['password']
#         try:
#             obj = models.UserInfo.objects.get(name=user)
#             if check_password(pwd, obj.password):
#                 request._request.session['is_login'] = True
#                 request._request.session['username'] = user
#                 print('-->check password',request._request.session['is_login'])
#                 return redirect('/')
#             else:
#                 msg = '密码错误'
#                 return render(request, 'login.html', {'msg': msg})
#         except UserInfo.DoesNotExist:
#             msg = 'user does not exist.'
#             return render(request, 'login.html', {'msg': msg})

# class Login(APIView):
#     def get(self,request,*args,**kwargs):
#         return render(request,'login.html',{'msg':''})
#     def post(self,request,*args,**kwargs):
#         username = request.data['username']
#         pwd = request.data['password']
#         print(username,pwd)
#         obj = models.User.objects.filter(name=username,password=pwd).first()
#         print('-->obj',obj)
#         if obj:
#             request._request.session['user_info'] = {'nid':obj.id,'username':obj.name}
#             MenuHelper(request,obj.name)
#             return redirect('/')
#         else:
#             return redirect('/login')

class LoginForm(forms.Form):
    username = forms.CharField(error_messages={'min_length':'长度不能小于6','required':'不能为空'},widget= \
        forms.TextInput(attrs={'placeholder': '用户名'}))
    # email = forms.CharField(error_messages={'required':'邮箱不能为空','invalid':'邮箱格式错误'},widget=\
    #     forms.EmailInput(attrs={'placeholder':'邮箱'}))
    password = fields.CharField(widget=forms.PasswordInput(attrs={'class':'c1','placeholder':'密码','required':'required'}),\
                               error_messages={'required':'密码不能为空'})
    # favor = forms.ChoiceField(
    #     choices=[(1,'watch TV'),(2,'music'),(3,'food')]
    # )

def login(request,*args,**kwargs):
    if request.method == 'GET':
        obj = LoginForm()
        return render(request, 'login.html', {'oo':obj})
    if request.method == 'POST':
        obj = LoginForm(request.POST)
        if obj.is_valid():
            data = obj.clean()
            print('-->data',data)
            obj = models.User.objects.filter(name=data['username'], password=data['password']).first()
            request.session['user_info'] = {'nid':obj.id,'username':obj.name}
            MenuHelper(request,obj.name)
            print(obj)
            return redirect('/')
        else:
            from django.forms.utils import ErrorDict
            print(obj.errors.as_data())
            # print(obj.errors['username'][0])
            # print(obj.errors['email'][0])
            # print(obj.data.getlist('username'))
            return render(request, 'login.html', {'oo':obj})


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

# @auth
# def index(request):
#     current_user = request.session.get('username')
#     print('-->current_user',current_user)
#     obj = models.User.objects.get(name=current_user)
#     user2role_list = models.User2Role.objects.filter(u=obj)
#     role_list= models.Role.objects.filter(user2role__u__name=current_user)
#     print(role_list)
#     # p2a2r_list = models.Permission2Action2Role.objects.filter(r__in=role_list)
#     menu_leaf_list = models.Permission2Action.objects.\
#         filter(permission2action2role__r__in=role_list).exclude(p__menu__isnull=True).\
#         values('p_id','p__url','p__caption','p__menu').distinct()
#     print(menu_leaf_list)
#     menu_leaf_dict = {}
#     for item in menu_leaf_list:
#         item = {
#             'id': item['p_id'],
#             'url': item['p__url'],
#             'caption': item['p__caption'],
#             'parent_id': item['p__menu'],
#             'child':[],
#             'status':True
#         }
#         if item['parent_id'] in menu_leaf_dict:
#             menu_leaf_dict[item['parent_id']].append(item)
#         else:
#             menu_leaf_dict[item['parent_id']] = [item]
#     print('-->menu_leaf_dict',menu_leaf_dict)
#     for item,v in menu_leaf_dict.items():
#         print('-->leaf item',v)
#     menu_list = models.Menu.objects.values('id','caption','parent_id')
#     print('-->menu_list',menu_list)
#     menu_dict = {}
#     for item in menu_list:
#         item['child'] = []
#         item['status'] = False
#         menu_dict[item['id']] = item
#
#     for k,v in menu_leaf_dict.items():
#         menu_dict[k]['child'] = v
#         parent_id = k
#         while parent_id:
#             menu_dict[parent_id]['status'] = True
#             parent_id = menu_dict[parent_id]['parent_id']
#     print('-------------- ')
#     for k,v in menu_dict.items():
#         print(k,v)
#     print(json.dumps(menu_dict,ensure_ascii=False))
#     for k,v in menu_leaf_dict.items():
#         print(k,v)
#     result = []
#     for row in menu_list:
#         if not row['parent_id']:
#             result.append(row)
#         else:
#             menu_dict[row['parent_id']]['child'].append(row)
#
#     print('------------------')
#     for item in result:
#         print(item)
#     string = menu_tree(result)
#     return render(request,'index.html',{'username':current_user,'menu_string':string})

def permission(func):
    def inner(request,*args,**kwargs):
        user_info = request.session.get('user_info')
        print('-->userinfo', user_info)
        if not user_info:
            return redirect('/login')
        obj = MenuHelper(request, user_info['username'])
        action_list = obj.actions()
        print('action_list', action_list)
        if not action_list:
            return HttpResponse('无权限访问')
        kwargs['xxx'] = 'this is a test.'
        print('-->kwargs',kwargs)
        kwargs['menu_string'] = obj.menu_tree()
        kwargs['action_list'] = obj.actions()
        kwargs['username'] = user_info['username']
        return func(request,*args,**kwargs)
    return inner

@permission
def index(request,*args,**kwargs):
    menu_string = kwargs.get('menu_string')
    action_list = kwargs.get('action_list')
    current_user = kwargs.get('username')
    if 'GET' in action_list:
        result = models.User.objects.all()
    else:
        result = []
    return render(request, 'index.html', {'username':current_user, 'menu_string':menu_string, 'action_list':action_list})

@permission
def test(request,*args,**kwargs):
    menu_string = kwargs.get('menu_string')
    action_list = kwargs.get('action_list')
    return render(request, 'test.html', {'menu_string':menu_string, 'action_list':action_list})

@permission
def jquery(request,*args,**kwargs):
    menu_string = kwargs.get('menu_string')
    action_list = kwargs.get('action_list')
    return render(request, 'jquery.html', {'menu_string':menu_string, 'action_list':action_list})

@permission
def tab(request,*args,**kwargs):
    menu_string = kwargs.get('menu_string')
    action_list = kwargs.get('action_list')
    return render(request, 'tab.html', {'menu_string':menu_string, 'action_list':action_list})

@permission
def top(request,*args,**kwargs):
    menu_string = kwargs.get('menu_string')
    action_list = kwargs.get('action_list')
    return render(request, 'top.html', {'menu_string':menu_string, 'action_list':action_list})

@permission
def ipinfo(request,*args,**kwargs):
    menu_string = kwargs.get('menu_string')
    action_list = kwargs.get('action_list')
    return render(request, 'ipinfo.html', {'menu_string':menu_string, 'action_list':action_list})

def menu_content(child_list):
    response = ''
    tpl = '''<div class="item">
        <div class="title">%s</div>
        <div class="content">%s</div>
    </div>'''
    for row in child_list:
        if not row['status']:
            continue
        if 'url' in row:
            response += '<a href="%s">%s</a>' % (row['url'],row['caption'])
        else:
            title = row['caption']
            content = menu_content(row['child'])
            response += tpl % (title,content)
    return response


# def menu_tree(result):
#     response = ''
#     tpl = '''<div class="item">
#         <div class="title">%s</div>
#         <div class="content">%s</div>
#     </div>'''
#     for row in result:
#         if not row['status']:
#             continue
#         title = row['caption']
#         content = menu_content(row['child'])
#         response += tpl % (title,content)
#     return response

class MenuHelper(object):
    def __init__(self,request,username):
        self.request = request
        self.username = username
        self.current_url = request.path_info
        self.permission2action_dict = None
        self.menu_leaf_list = None
        self.menu_list = None
        self.session_data()

    def session_data(self):
        permission_dict = self.request.session.get('permission_info')
        if permission_dict:
            self.permission2action_dict = permission_dict['permission2action_dict']
            self.menu_leaf_list = permission_dict['menu_leaf_list']
            self.menu_list = permission_dict['menu_list']
        else:
            role_list = models.Role.objects.filter(user2role__u__name=self.username)
            permission2action_list = models.Permission2Action.objects.\
                filter(permission2action2role__r__in=role_list).exclude(p__menu__isnull=True).\
                values('p__url','a__code').distinct()
            permission2action_dict = {}
            for item in permission2action_list:
                if item['p__url'] in permission2action_dict:
                    permission2action_dict[item['p__url']].append(item['a__code'])
                else:
                    permission2action_dict[item['p__url']] = [item['a__code']]

            menu_leaf_list = list(models.Permission2Action.objects.\
                filter(permission2action2role__r__in=role_list).exclude(p__menu__isnull=True).\
                values('p_id','p__url','p__caption','p__menu').distinct())
            menu_list = list(models.Menu.objects.values('id','caption','parent_id'))

            self.request.session['permission_info'] = {
                'permission2action_dict': permission2action_dict,
                'menu_leaf_list': menu_leaf_list,
                'menu_list': menu_list,
            }

    def menu_data_list(self):
        menu_leaf_dict = {}
        open_leaf_parent_id = None
        for item in self.menu_leaf_list:
            item = {
                'id': item['p_id'],
                'url': item['p__url'],
                'caption': item['p__caption'],
                'parent_id': item['p__menu'],
                'child':[],
                'status':True
            }
            if item['parent_id'] in menu_leaf_dict:
                menu_leaf_dict[item['parent_id']].append(item)
            else:
                menu_leaf_dict[item['parent_id']] = [item]
        print('-->menu_leaf_dict',menu_leaf_dict)
        menu_dict = {}
        for item in self.menu_list:
            item['child'] = []
            item['status'] = False
            menu_dict[item['id']] = item

        for k,v in menu_leaf_dict.items():
            menu_dict[k]['child'] = v
            parent_id = k
            while parent_id:
                menu_dict[parent_id]['status'] = True
                parent_id = menu_dict[parent_id]['parent_id']

        while open_leaf_parent_id:
            menu_dict[open_leaf_parent_id]['open'] = True
            open_leaf_parent_id = menu_dict[open_leaf_parent_id]['parent_id']

        result = []
        for row in menu_dict.values():
            if not row['parent_id']:
                result.append(row)
            else:
                menu_dict[row['parent_id']]['child'].append(row)

        return result

    def menu_content(self,child_list):
        response = ''
        tpl = '''<div class="item">
            <div class="title">%s</div>
            <div class="content">%s</div>
        </div>'''
        for row in child_list:
            if not row['status']:
                continue
            if 'url' in row:
                response += '<a href="%s">%s</a>' % (row['url'], row['caption'])
            else:
                title = row['caption']
                content = self.menu_content(row['child'])
                response += tpl % (title, content)
        return response

    def menu_tree(self):
        response = ''
        tpl = '''<div class="item">
            <div class="title">%s</div>
            <div class="content">%s</div>
        </div>'''
        for row in self.menu_data_list():
            if not row['status']:
                continue
            title = row['caption']
            content = self.menu_content(row['child'])
            response += tpl % (title, content)
        return response


    def actions(self):
        action_list = []
        for k,v in self.permission2action_dict.items():
            print('action k v',k,v)
            print('-->current_url',self.current_url)
            if re.match(k,self.current_url):
                action_list = v
                break
        return action_list

# @auth
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
        return render(request, 'classes.html', {'username':current_user, 'classes':cls_list, 'str_pager':pager})
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


def edit_class(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        obj = models.Classes.objects.filter(id=nid).first()
        return render(request, 'edit_class.html', {'obj':obj})
    elif request.method == 'POST':
        nid = request.POST.get('nid')
        caption = request.POST.get('caption')
        models.Classes.objects.filter(id=nid).update(caption=caption)
        return redirect('/classes')
    else:
        return redirect('/')

def make_data():
    from subprocess import Popen, PIPE

    def exec_cmd(cmd):
        res = Popen(cmd, shell=True, stdout=PIPE)
        ret = res.communicate()[0].decode('utf-8')
        return ret

    cmd = 'curl -H "X-Consul-Token: blizzmi.us007" -s -G http://192.168.200.60:8500/v1/agent/services|json'
    services = exec_cmd(cmd)
    data = []
    for item in json.loads(services):
        data.append({'title': item})

    newdata = 'var data1 = %s' % data
    from s7day129 import settings
    filename = os.path.join(settings.BASE_DIR, 'static/js/data.js')
    print(filename)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(newdata)

@permission
def del_consul(request,*args,**kwargs):
    menu_string = kwargs.get('menu_string')
    action_list = kwargs.get('action_list')
    if request.method == 'GET':
        make_data()
        print('新数据')
        return render(request, 'del_consul.html', {'menu_string':menu_string,\
                                           'action_list':action_list})
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
    return render(request, 'teacher.html', {'username':username, 'teachers':result})

def add_teacher(request):
    if request.method == 'GET':
        cls_list = models.Classes.objects.all()
        return render(request, 'add_teacher.html', {'cls_list':cls_list})
    elif request.method == 'POST':
        teacher = request.POST.get('teacher')
        cls = request.POST.getlist('cls')
        print('-->cls',cls)
        obj = models.Teacher.objects.create(name=teacher)
        obj.cls.add(*cls)
        return redirect('/teacher')


def edit_teacher(request,nid):
    if request.method == 'GET':
        obj = models.Teacher.objects.get(id=nid)
        obj_cls_list = obj.cls.all().values_list('id','caption')
        print(bool(obj_cls_list))
        id_list = list(zip(*obj_cls_list))[0] if obj_cls_list else []
        print('-->id_list',id_list)
        cls_list = models.Classes.objects.exclude(id__in=id_list)
        print('-->cls_list',cls_list)
        return render(request, 'edit_teacher.html', {'obj':obj, 'id_list':id_list, 'cls_list':obj_cls_list, 'exclude_list':cls_list})
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
    return render(request, 'modal.html')


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
            return render(request, 'register/reg.html', {"username": username, "passwd": passwd, "name":name})
        else:
            return render(request, 'register/reg.html', {"username": username, "passwd": passwd, "hidden2": "hidden", "name":name})
    else:
        return render(request, 'register/reg.html', {"hidden": "hidden"})

def check_name(name):
    getUrl = 'https://api.bearychat.com/v1/user.list?token=049ecceaea09856c86236fef0068c8d6'
    req_info = requests.get(getUrl).json()
    for i in req_info:
        if (i['name'] == name or i['full_name'] == name) and i['inactive'] == False:
            return True

@permission
def dropuser(request,*args,**kwargs):
    menu_string = kwargs.get('menu_string')
    action_list = kwargs.get('action_list')
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
        return render(request, 'register/dropuser.html', {"hidden": "hidden", 'username':user, 'menu_string':menu_string})

def upload(request,*args,**kwargs):
    menu_string = kwargs.get('menu_string')
    action_list = kwargs.get('action_list')
    if request.method == 'GET':
        return render(request, 'ops/upload.html',{'menu_string':menu_string})
    elif request.method == 'POST':
        obj = request.FILES.get('file')
        if obj:
            if re.findall('[()]',obj.name):
                print('-->此处括号')
                msg = '上传失败!文件名不要使用括号等特殊字符!'
                return JsonResponse({"status":False,"msg":msg})
                #return render(request,'ops/upload.html',{'msg':msg})
            file_path = os.path.join('/var/www/html/upload',obj.name)
            f = open(file_path,'wb')
            for chunk in obj.chunks():
                f.write(chunk)
            f.close
            print('-->file_path',file_path)
            print('-->obj',obj)
            if os.path.exists(file_path):
                #howbig = int(exec_cmd("stat -c '%s' {0}".format(file_path)))
                md5 = exec_cmd('md5sum %s' % file_path).split()[0]
                print('-->md5',md5)
                new_name = md5[:8]+'_'+obj.name
                new_file_path = os.path.dirname(file_path)+'/'+new_name
                print('-->new_file_path',new_file_path)
                os.rename(file_path,new_file_path)
                howbig = obj.size / 1024 / 1024
                howbig = round(howbig,2)
                internet_add = 'http://sz.v26.top:18081/' + new_name
                print('-->internet_add',internet_add)
                ret = {"status":True,"howbig":howbig,"md5":md5,"internet_add":internet_add,"name":obj.name}
                return JsonResponse(ret)
                #return render(request,'ops/upload.html',{'msg':'上传成功','howbig':howbig,'md5':md5,'internet_add':internet_add,'name':obj.name})
            else:
                return JsonResponse({'status':False})
        else:
            return render(request, 'ops/upload.html',{'msg':'请选择文件'})

def search(request):
    if request.method == 'GET':
        q = request.GET.get('q')
        print(q)
        objs = models.Classes.objects.filter(caption__contains=q)
        l = [ obj.caption for obj in objs ]
        print(l)

        return JsonResponse(l,safe=False)

@permission
def add_consul(request,*args,**kwargs):
    menu_string = kwargs.get('menu_string')
    action_list = kwargs.get('action_list')
    user = request.session.get('username')
    service = {}
    if request.method == 'GET':
        return render(request, 'add_consul.html', {'username':user, 'menu_string':menu_string,\
                                           'action_list':action_list
                                                   })
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

@permission
def compare(request,*args,**kwargs):
    menu_string = kwargs.get('menu_string')
    print('-->compare',menu_string)
    action_list = kwargs.get('action_list')
    if request.method == 'GET':
        user = request.session.get('username')
        accounts = account_compare()
        print('-->accounts',accounts)
        return render(request, 'compare.html', {'accounts':accounts,
                                               'username':user,
                                               'menu_string':menu_string,
                                               'action_list':action_list})


def blur(request):
    # q = request.GET['q']
    # models.Classes.objects.filter(caption__contains=q)
    # objs = models.Classes.objects.filter(caption__contains=q)
    # l = [obj.caption for obj in objs]
    # print(l)
    return render(request, 'blur.html')

def file_md5(path):
    md5 = hashlib.md5()
    path_size = os.path.getsize(path)
    with open(path,'rb') as f:
        while path_size >= 4096:
            cont = f.read(4096)
            md5.update(cont)
            path_size -= 4096
        else:
            cont = f.read()
            if cont:
                md5.update(cont)
    return md5.hexdigest()

@permission
def ftp(request,*args,**kwargs):
    if request.method == 'GET':
        user = request.session.get('username')
        # pictures = models.Img.objects.all()
        return render(request, 'ftp.html', {'username':user})
    elif request.method == 'POST':
        obj = request.FILES.get('transfer')
        if obj:
            file_path = os.path.join('static','upload',obj.name)
            f = open(file_path,'wb')
            for chunk in obj.chunks():
                f.write(chunk)
            f.close
            print('-->file_path',file_path)

            if os.path.exists(file_path):
                md5 = exec_cmd('md5sum %s' % file_path)
                print('-->md5',md5)
                sep = file_path.split('.')
                file_name = '.'.join((sep[0]+'_'+md5[:8],sep[1]))
                print('-->file_name',file_name)
                os.rename(file_path,file_name)
                print('上传文件大小')
                local_add = 'http://192.168.200.111:18081/' + file_name
                internet_add = 'http://218.17.239.26:18081/'+ file_name

                return render(request, 'ftp.html', {'msg': '请选择文件', 'md5':md5, 'local_add':local_add, 'internet_add':internet_add})
        else:
            return render(request, 'ftp.html', {'msg': '请选择文件'})








