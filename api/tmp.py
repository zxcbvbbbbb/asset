x = [(1, '空闲'), (2, '使用'), (3, '报废')]

temp = []
for i in x:
    t = list(i)
    t[0] = t[1]
    temp.append(t)



