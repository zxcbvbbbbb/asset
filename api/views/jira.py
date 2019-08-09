from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from .views import permission
from api import models
import pymysql

def query(sql):
    db = pymysql.connect("192.168.200.150", "root", "wefw$jh374SDYU", "jiradb")
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

    except:
        print("Error: unable to fetch data")
    db.close()

@permission
def staff_month(request,*args,**kwargs):
    menu_string = kwargs.get('menu_string')
    action_list = kwargs.get('action_list')
    current_user = kwargs.get('username')
    if request.method == 'GET':
        return render(request, 'staff_month.html', {'username':current_user, 'menu_string':menu_string, 'action_list':action_list})
    elif request.method == 'POST':
        start = '"'+ request.POST.get('start') + '"'
        end = '"'+ request.POST.get('end') + '"'
        sql = '''
            select aa.`项目`,aa.`姓名`,aa.`耗时H`,format(aa.`耗时H` / bb.`总计`, 3) as 百分比 from 
            (SELECT d.pname as 项目,c.姓名,format(sum(c.耗时) / 60 / 60, 2) as 耗时H from (
            (SELECT a.项目ID,a.任务名称,b.display_name as 姓名,a.耗时,a.解决时间 FROM (
            (SELECT project as 项目ID, summary as 任务名称,assignee as 经办人ID,TIMESPENT AS 耗时,RESOLUTIONDATE as 解决时间 from jiraissue where
             RESOLUTIONDATE BETWEEN {0} AND {1} and TIMESPENT is not NULL) as a 
            LEFT JOIN cwd_user AS b ON a.经办人ID = b.lower_user_name
            )) as c 
            LEFT JOIN project as d on c.项目ID = d.id
            )
            GROUP BY c.姓名,c.项目ID
            ORDER BY c.项目ID) as aa
            LEFT JOIN
            (SELECT c.姓名,format(sum(c.耗时) / 60 / 60, 2) as 总计 from (
            (SELECT a.项目ID,a.任务名称,b.display_name as 姓名,a.耗时,a.解决时间 FROM (
            (SELECT project as 项目ID, summary as 任务名称,assignee as 经办人ID,TIMESPENT AS 耗时,RESOLUTIONDATE as 解决时间 from jiraissue where
             RESOLUTIONDATE BETWEEN {0} AND {1} and TIMESPENT is not NULL) as a 
            LEFT JOIN cwd_user AS b ON a.经办人ID = b.lower_user_name
            )) as c 
            LEFT JOIN project as d on c.项目ID = d.id
            )
            GROUP BY c.姓名) as bb
            on aa.`姓名` = bb.`姓名`

            order by aa.`姓名`
        '''.format(start, end)
        rep = query(sql)
        return render(request, 'staff_month.html',{'username':current_user, 'menu_string':menu_string, 'action_list':action_list,'data':list(rep)})

@permission
def staff_season(request,*args,**kwargs):
    menu_string = kwargs.get('menu_string')
    action_list = kwargs.get('action_list')
    current_user = kwargs.get('username')
    if request.method == 'GET':
        return render(request, 'staff_season.html', {'username':current_user, 'menu_string':menu_string, 'action_list':action_list})
    elif request.method == 'POST':
        start = '"'+ request.POST.get('start') + '"'
        end = '"'+ request.POST.get('end') + '"'
        sql = '''
            select aa.`项目`,aa.`姓名`,aa.`耗时H`,format(aa.`耗时H` / 528, 3) as 百分比 from 
            (SELECT d.pname as 项目,c.姓名,format(sum(c.耗时) / 60 / 60, 2) as 耗时H from (
            (SELECT a.项目ID,a.任务名称,b.display_name as 姓名,a.耗时,a.解决时间 FROM (
            (SELECT project as 项目ID, summary as 任务名称,assignee as 经办人ID,TIMESPENT AS 耗时,RESOLUTIONDATE as 解决时间 from jiraissue where
             RESOLUTIONDATE BETWEEN "2018-04-01" AND "2018-07-01" and TIMESPENT is not NULL) as a 
            LEFT JOIN cwd_user AS b ON a.经办人ID = b.lower_user_name
            )) as c 
            LEFT JOIN project as d on c.项目ID = d.id
            )
            GROUP BY c.姓名,c.项目ID
            ORDER BY c.项目ID) as aa
            LEFT JOIN
            (SELECT c.姓名,format(sum(c.耗时) / 60 / 60, 2) as 总计 from (
            (SELECT a.项目ID,a.任务名称,b.display_name as 姓名,a.耗时,a.解决时间 FROM (
            (SELECT project as 项目ID, summary as 任务名称,assignee as 经办人ID,TIMESPENT AS 耗时,RESOLUTIONDATE as 解决时间 from jiraissue where
             RESOLUTIONDATE BETWEEN "2018-04-01" AND "2018-07-01" and TIMESPENT is not NULL) as a 
            LEFT JOIN cwd_user AS b ON a.经办人ID = b.lower_user_name
            )) as c 
            LEFT JOIN project as d on c.项目ID = d.id
            )
            GROUP BY c.姓名) as bb
            on aa.`姓名` = bb.`姓名`
            
            order by aa.`姓名`
        '''.format(start, end)
        rep = query(sql)
        return render(request, 'staff_season.html',{'username':current_user, 'menu_string':menu_string, 'action_list':action_list,'data':list(rep)})


@permission
def finance_staff_month(request, *args, **kwargs):
    menu_string = kwargs.get('menu_string')
    action_list = kwargs.get('action_list')
    current_user = kwargs.get('username')
    if request.method == 'GET':
        return render(request, 'finance_staff_month.html',
                      {'username': current_user, 'menu_string': menu_string, 'action_list': action_list})
    elif request.method == 'POST':
        start = '"' + request.POST.get('start') + '"'
        end = '"' + request.POST.get('end') + '"'
        sql = '''
            select aa.`项目`,aa.`姓名`,aa.`耗时H`,format(aa.`耗时H` / bb.`总计`, 3) as 百分比 from 
            (SELECT d.pname as 项目,c.姓名,format(sum(c.耗时) / 60 / 60, 2) as 耗时H from (
            (SELECT a.项目ID,a.任务名称,b.display_name as 姓名,a.耗时,a.解决时间 FROM (
            (SELECT project as 项目ID, summary as 任务名称,assignee as 经办人ID,TIMESPENT AS 耗时,RESOLUTIONDATE as 解决时间 from jiraissue where
             RESOLUTIONDATE BETWEEN "2019-4-01" AND "2019-5-01" and TIMESPENT is not NULL) as a 
            LEFT JOIN cwd_user AS b ON a.经办人ID = b.lower_user_name
            )) as c 
            LEFT JOIN project as d on c.项目ID = d.id
            )
            GROUP BY c.姓名,c.项目ID
            ORDER BY c.项目ID) as aa
            LEFT JOIN
            (SELECT c.姓名,format(sum(c.耗时) / 60 / 60, 2) as 总计 from (
            (SELECT a.项目ID,a.任务名称,b.display_name as 姓名,a.耗时,a.解决时间 FROM (
            (SELECT project as 项目ID, summary as 任务名称,assignee as 经办人ID,TIMESPENT AS 耗时,RESOLUTIONDATE as 解决时间 from jiraissue where
             RESOLUTIONDATE BETWEEN "2019-4-01" AND "2019-5-01" and TIMESPENT is not NULL) as a 
            LEFT JOIN cwd_user AS b ON a.经办人ID = b.lower_user_name
            )) as c 
            LEFT JOIN project as d on c.项目ID = d.id
            )
            GROUP BY c.姓名) as bb
            on aa.`姓名` = bb.`姓名`
            
            order by aa.`姓名`
        '''.format(start, end)
        rep = query(sql)
        return render(request, 'finance_staff_month.html',
                      {'username': current_user, 'menu_string': menu_string, 'action_list': action_list,
                       'data': list(rep)})
