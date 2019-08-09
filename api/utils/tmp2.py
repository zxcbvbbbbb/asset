import pymysql

def mysql():
    db = pymysql.connect("192.168.200.150", "root", "wefw$jh374SDYU", "jiradb")
    cursor = db.cursor()

    sql = '''
        select aa.`项目`,aa.`姓名`,aa.`耗时H`,format(aa.`耗时H` / bb.`总计`, 3) as 百分比 from 
        (SELECT d.pname as 项目,c.姓名,format(sum(c.耗时) / 60 / 60, 2) as 耗时H from (
        (SELECT a.项目ID,a.任务名称,b.display_name as 姓名,a.耗时,a.解决时间 FROM (
        (SELECT project as 项目ID, summary as 任务名称,assignee as 经办人ID,TIMESPENT AS 耗时,RESOLUTIONDATE as 解决时间 from jiraissue where
         RESOLUTIONDATE BETWEEN "2019-04-01" AND "2019-05-01" and TIMESPENT is not NULL) as a 
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
         RESOLUTIONDATE BETWEEN "2019-04-01" AND "2019-05-01" and TIMESPENT is not NULL) as a 
        LEFT JOIN cwd_user AS b ON a.经办人ID = b.lower_user_name
        )) as c 
        LEFT JOIN project as d on c.项目ID = d.id
        )
        GROUP BY c.姓名) as bb
        on aa.`姓名` = bb.`姓名`
        
        order by aa.`姓名`
    '''
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        for item in results:
            print(item)

    except Exception as e:
        print("Error: unable to fetch data")
        print(e)
    db.close()

mysql()