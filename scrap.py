import requests
from bs4 import BeautifulSoup



u1 = 'https://book.douban.com/subject_search?search_text=%E6%95%B0%E6%8D%AE&cat=1001'

r = requests.get(url=u1)
r.encoding = r.apparent_encoding

#获取heards
dic_h = {'user-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}


#获取cookies
cookies = 'bid=o7Q3ROIIEiM; ap_v=0,6.0; __utma=30149280.154571472.1568124005.1568124005.1568124005.1; __utmc=30149280; __utmz=30149280.1568124005.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=81379588.1910030307.1568124005.1568124005.1568124005.1; __utmc=81379588; __utmz=81379588.1568124005.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=%E8%B1%86%E7%93%A3; gr_user_id=c498dd0d-6f4b-4439-841a-d08a6e2d579c; gr_cs1_a393a104-3444-48e2-9cd0-05c271a711b5=user_id%3A0; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1568124005%2C%22https%3A%2F%2Fwww.baidu.com%2Fs%3Fwd%3D%25E8%25B1%2586%25E7%2593%25A3%26rsv_spt%3D1%26rsv_iqid%3D0xe5249f3f00029890%26issp%3D1%26f%3D8%26rsv_bp%3D1%26rsv_idx%3D2%26ie%3Dutf-8%26rqlang%3Dcn%26tn%3Dbaiduhome_pg%26rsv_enter%3D1%26rsv_dl%3Dtb%26oq%3Dmac%2525E5%2525AE%252589%2525E8%2525A3%252585vscode%26inputT%3D3660%26rsv_t%3D836erG0wNVO2v8Lp4CwMQ0OT2lRohicLTEcxqL9x7D%252BSWtZMjzqaZcTbRlUvz9eVtWVf%26rsv_pq%3De41b1e2c000246fa%26rsv_sug3%3D48%26rsv_sug1%3D38%26rsv_sug7%3D100%26rsv_sug2%3D0%26rsv_sug4%3D4368%22%5D; _pk_ses.100001.3ac3=*; __yadk_uid=URDQzf6i95Pgq0sWZJJ9uuACx8FlliXW; _vwo_uuid_v2=D02FD04EF9327A7BD9512721CC216745E|067e8d16c631b0c51685e9ed51508863; viewed="10799984"; __utmb=81379588.3.10.1568124005; __utmt=1; dbcl2="148492991:QU3mFJ1ZG44"; ck=vJYE; push_noty_num=0; push_doumail_num=0; __utmv=30149280.14849; _pk_id.100001.3ac3=be5db9c252694557.1568124005.1.1568125861.1568124005.; __utmb=30149280.13.10.1568124005'
clst = cookies.split('; ')
dic_c = {}
for i in clst:
	# print(dic_c[i.split('=')[0]])
	dic_c[i.split('=')[0]] = i.split('=')[1]


r1 = requests.get(url=u1,headers = dic_h,cookies = dic_c)
soup = BeautifulSoup(r1.text,'lxml')


