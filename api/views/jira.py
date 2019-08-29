from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from .views import permission
from api import models
import pymysql,time,math

def query(sql,database):
    db = pymysql.connect("192.168.200.150", "root", "wefw$jh374SDYU", "%s" % database)
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
        rep = query(sql,"jiradb")
        print('->staff_month',list(rep))
        '''[('MChat', '万锦龙', '16.00', '1.000'), ('Chess-UIS', '何嘉辉', '8.00', '1.000'), ('运维组', '何少东', '41.00', '1.000'), ('CRM', '何桂平', '4.00', '1.000'), ('SLOT-EA', '冯令源', '24.00', '1.000'), ('MChat', '刘云', '8.00', '1.000'), ('Chess-UIS', '刘柳楷', '24.00', '1.000'), ('SLOT-EA', '包蕊洁', '8.00', '1.000'), ('FG-Hunter', '向召华', '16.00', '1.000'), ('FG-Hunter', '周柏森', '89.00', '1.000'), ('运维组', '孙善武', '36.00', '1.000'), ('MChat', '孙艺盟', '32.00', '1.000'), ('FG-Hunter', '宁国强', '40.00', '1.000'), ('Chess-UIS', '宋浩冰', '16.00', '1.000'), ('SLOT-EA', '尹致远', '24.00', '1.000'), ('SLOT-EA', '庄婷婷', '16.00', '1.000'), ('FG-Hunter', '廖宁欢', '14.00', '1.000'), ('FG-Hunter', '廖文臣', '40.00', '1.000'), ('美术组', '张业莉', '24.00', '1.000'), ('FG-Hunter', '张利华', '32.00', '1.000'), ('美术组', '张芳翠', '36.00', '1.000'), ('PLATFORM-NEW', '张震', '16.00', '1.000'), ('FG-Hunter', '戴诗静', '136.00', '1.000'), ('PLATFORM-NEW', '李建明', '10.00', '1.000'), ('FG-Hunter', '李新', '4.00', '1.000'), ('CRM', '李汉标', '8.00', '1.000'), ('Chess-UIS', '李通', '3.00', '1.000'), ('PLATFORM-NEW', '杨灿才', '8.00', '1.000'), ('美术组', '梁冠生', '18.00', '1.000'), ('Chess-UIS', '梁良', '40.00', '1.000'), ('MChat', '欧喜荣', '24.00', '1.000'), ('SLOT-EA', '欧阳高峰', '14.40', '0.333'), ('美术组', '欧阳高峰', '28.80', '0.667'), ('Chess-UIS', '王昭君', '40.00', '1.000'), ('MChat', '王枭波', '16.00', '1.000'), ('MChat', '甘俊贤', '40.00', '1.000'), ('Chess-UIS', '詹家耿', '16.00', '1.000'), ('MChat', '谌兆林', '24.00', '1.000'), ('FG-Hunter', '谢标', '32.00', '1.000'), ('Chess-UIS', '贺业臣', '40.00', '1.000'), ('MChat', '邓伟苹', '40.00', '1.000'), ('Chess-UIS', '邓智辉', '32.00', '1.000'), ('MChat', '邓远明', '1.00', '1.000'), ('FG-Hunter', '阮上栩', '12.00', '1.000'), ('Chess-UIS', '陈光明', '2.00', '1.000'), ('Chess-UIS', '陈鸿艺', '40.00', '1.000'), ('Chess-UIS', '鲁明', '24.00', '1.000'), ('FG-Hunter', '黄家乐', '56.00', '1.000'), ('CRM', '黄梓泓', '20.00', '1.000'), ('SLOT-EA', '黄锦孝', '16.00', '1.000')]'''
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
        rep = query(sql,"jiradb")
        return render(request, 'staff_season.html',{'username':current_user, 'menu_string':menu_string, 'action_list':action_list,'data':list(rep)})

def time_transfer(timestr):
    t = time.strptime(timestr, '%Y-%m-%d')
    return math.floor(time.mktime(t))

@permission
def bug_count(request, *args, **kwargs):
    menu_string = kwargs.get('menu_string')
    action_list = kwargs.get('action_list')
    current_user = kwargs.get('username')
    if request.method == 'GET':
        return render(request, 'bug_count.html',
                      {'username': current_user, 'menu_string': menu_string, 'action_list': action_list})
    elif request.method == 'POST':
        start_time = request.POST.get('start')
        s = time.strptime(start_time,'%Y-%m-%d')
        start = math.floor(time.mktime(s))
        print('-->start',start)
        end_time = request.POST.get('end')
        e = time.strptime(end_time,'%Y-%m-%d')
        end = math.floor(time.mktime(e))
        print('-->end', end)
        sql = '''
            SELECT
                    mantis_category_table.name as 史诗,
                mantis_user_table.realname as 经办人,
                CASE x.severity
            WHEN 50 THEN
                "致命A"
            WHEN 40 THEN
                "严重B"
            WHEN 30 THEN
                "普通C"
            WHEN 20 THEN
                "轻微D"
            WHEN 10 THEN
                "建议E"
            ELSE
                "OTHER"
            END AS 严重性,
             Count(x.severity) AS 该时段bug数
            FROM
                (SELECT * from (SELECT b.*,c.`value` AS ENV from mantis_bug_table as b LEFT JOIN mantis_custom_field_string_table as c on b.id = c.bug_id) AS a where a.ENV in ("SIT","UAT","PRO")) as x,mantis_user_table,mantis_category_table
            WHERE
            mantis_user_table.id = x.handler_id AND mantis_category_table.id = x.category_id AND
                x.date_submitted BETWEEN {0} AND {1}
            GROUP BY
                category_id,mantis_user_table.realname,x.severity
            ORDER BY mantis_user_table.realname,category_id,x.severity
        '''.format(start, end)
        print('-->sql',sql)
        rep = query(sql,'mantis')
        return render(request, 'bug_count.html',
                      {'username': current_user, 'menu_string': menu_string, 'action_list': action_list,
                       'data': list(rep)})
