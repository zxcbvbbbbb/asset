
with open('tmp.txt','r',encoding='utf-8') as f:
    for name in f.readlines():
        print(name.strip())

# from api import models
# models.Employee.objects.create(name='test',dept_id=1)