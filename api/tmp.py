import xlrd
from datetime import datetime

data = xlrd.open_workbook('asset.xlsx')
table = data.sheet_by_name('电脑设备')
for i in range(table.nrows):
    if type(table.row_values(i)[0]) is float:
        x = xlrd.xldate_as_datetime(table.row_values(i)[0],0)
        table.row_values(i)[0] = x.strftime('%Y-%m-%d')
        print(table.row_values(i))
    else:
        print('xx')
    # print(xlrd.xldate_as_datetime(table.row_values(i)[0],0))
