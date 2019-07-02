#display，width，text-align
例1：
https://www.runoob.com/css/css-display-visibility.html  
把列表项显示为内联元素：
li {display:inline;}

例2:
s7day57的作业
用户名密码登录框设置为inline-block才能对齐

        label {
            width: 80px;
            text-align: right;
            display: inline-block;
        }
        }

#59-03：
django支持CBV,FBV；
将登录FBV改成CBV

#59-04
1.FBV与CBV的装饰器写法不一样；
from django.views import VIEW
执行CBV的方法前会先执行VIEW的dispatch方法(分发器，get或post等方法执行完后会把数据给它，所以dispatch需要return数据)，也可以自定义dispatch；
dispatch方法相当于FBV装饰器(@auth)的作用

2.
CBV的Login要写get方法，否则访问/login会405 not allowed





classes页面：
表格填什么内容？ID，标题，操作(编辑|删除,2个a标签)

模态对话框：
day47

#59-08
1.判断方法的原因
def handle_classes(request):
    if request.method == 'GET': (post提交时不需要做get里的操作)
		classes = models.Classes.objects.all()
		
2.寻找caption标签
    <div class="modal hide">
        <form method="post" action="/classes/">
            <input name="caption" type="text" placeholder="请输入标题">
            <input id="id_modal_cancel" type="button" value="取消">
            <input type="submit" value="确定">
            <input id="modal_ajax_submit" type="button" value="ajax确定">
        </form>
    </div>
	
$("[name='csrfmiddlewaretoken']").val()
$('.modal input[name="caption"]').val()
$('[name="caption"]').val()

3.获取caption值失败
function bindSubmitModal() {
	// var value = $('.modal input[name="caption"]').val() (写这里获取不到)
	$('#modal_ajax_submit').click(function () {
		var value = $('.modal input[name="caption"]').val()
		
4.刷新页面
location.reload()

#59-08
js事件委托
jiquery的on
$().on(click,function())
$().on(click,'xx',function())

#59-11
模态对话框提交，换成URL方式提交

#59-12
分页

1.数据库分片取数据
2.current_page,start_page,end_page表达式
3.classes?p=1的形式(后台传)
4.divmod取余

#59-18 新URL提交

#60-01 orm数据库操作

#60-04
获取老师列表1
teacher_list = models.Teacher.objects.all()，前端循环，操作数据库比较多

#60-07
获取老师列表3

    teacher_list = models.Teacher.objects.filter(id__in=models.Teacher.objects.all()[0:2]).values('id','name','cls__id','cls__caption')
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
		
#60-11
修改老师信息

1.
传老师id的方式：
url(r'^edit_teacher-(\d+)/$')
def edit_teacher(request,nid) #不需要从GET方法中取

2.
添加老师的input框 name='teacher'用来提交信息
编辑老师的input框 value="{{ obj.name }}"需要直接显示

3.
选中老师所教的班级：
    cls = obj.cls.all().values_list('id')
    id_list = list(zip(*cls))[0]
	
#61-03
给编辑老师的select设置一个id='sel'
在浏览器console直接获取选中的班级$('#sel').val()
    
jQuery对象和DOM对象
	obj = document.getElementById('sel')
	$(obj)
	
	$('#sel')
	$('#sel')[0]
	
	select标签的Dom对象中有 selectedOptions
	$('#sel')[0].selectedOptions
	
	appendTo
	
#61-04
提交前全选中：
	$('#submitForm').click(function () {
		$('#sel').children().each(function () {
			$(this).prop('selected',true)
		})
	})
	
#61-05
文件路径存到数据库里