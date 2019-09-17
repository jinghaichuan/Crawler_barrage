import re

lst = ['小红的成绩为98分',
	   '小王的成绩为92分',
	   '老李今天没上班',
	   '小明的成绩为88分'
	   ]

m = r'(\D*)的成绩为(\d*)分'
lst1 = []
for i in lst:
	matchob = re.match(m, i)
	dic = {}
	if matchob:
		dic['姓名'] = matchob.group(1)
		dic['成绩'] = matchob.group(2)
		lst1.append(dic)
	else:
		print('匹配失败')