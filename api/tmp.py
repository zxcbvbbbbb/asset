import xlrd
from datetime import datetime
from api import models

data = xlrd.open_workbook('d:/posttest/api/info.xlsx')
table = data.sheet_by_name('Sheet1')
style_list = []
for i in range(table.nrows):
    if type(table.row_values(i)[0]) is float and type(table.row_values(i)[1]) is float:
        x = xlrd.xldate_as_datetime(table.row_values(i)[0],0)
        y = xlrd.xldate_as_datetime(table.row_values(i)[1],0)
        data_list = table.row_values(i)
        data_list[0] = x.strftime('%Y-%m-%d')
        data_list[1] = y.strftime('%Y-%m-%d')
        employee_id = models.Employee.objects.filter(name=data_list[2]).first().id
        data_list[2] = employee_id
        style_id = models.Style.objects.filter(name=data_list[4]).first().id
        data_list[4] = style_id
        style_list.append(data_list[4])
    else:
        print('xx')
    # print(xlrd.xldate_as_datetime(table.row_values(i)[0],0))

print(data_list)