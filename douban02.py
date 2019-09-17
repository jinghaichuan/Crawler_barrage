import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def get_url(n):
	'''
	分页函数采集
	:param n: 页数参数
	:return: 得到一个分页网页的list
	'''
	lst = []
	for i in range(n):
		ui = 'https://book.douban.com/tag/%%E7%%94%%B5%%E5%%BD%%B1?start=%i&type=T' % (i * 20)
		lst.append(ui)
	return lst


def get_data(ui, d_h, d_c):
	'''
	数据采集
	:param ui:数据信息网页
	:param d_h: user-agent信息
	:param d_c: cookies信息
	:return: 得到数据的list，每条用dict存储
	'''
	ri = requests.get(url=ui, headers=d_h, cookies=d_c)
	soupi = BeautifulSoup(ri.text, 'lxml')

	ul = soupi.find('ul', class_="subject-list")
	lis = ul.find_all('li')

	lst = []
	for li in lis:
		dic = {}
		dic['书名'] = li.find('div', class_='info').h2.text.replace(' ', '').replace('\n', '')
		# dic['评分'] = li.find('span', class_='rating_nums').text
		# dic['评价人数'] = li.find('span', class_='pl').text.replace('\n', '').replace('(', '').replace('人评价)', '').replace(
		# 	' ', '')
		dic['评价'] = li.find('div',class_ = "star clearfix").text.replace(' ', '').replace('\n', '')
		dic['简介'] = li.find('p').text
		dic['其他信息'] = li.find('div', class_='pub').text.replace(' ', '').replace('\n', '')
		lst.append(dic)
	return lst


if __name__ == "__main__":
	urllst1 = get_url(10)

	dic_h = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
	dic_c = {}
	cookies = 'bid=o7Q3ROIIEiM; __utmz=81379588.1568124005.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=%E8%B1%86%E7%93%A3; gr_user_id=c498dd0d-6f4b-4439-841a-d08a6e2d579c; __yadk_uid=URDQzf6i95Pgq0sWZJJ9uuACx8FlliXW; _vwo_uuid_v2=D02FD04EF9327A7BD9512721CC216745E|067e8d16c631b0c51685e9ed51508863; viewed="10799984"; dbcl2="148492991:QU3mFJ1ZG44"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.14849; __utmz=30149280.1568211966.3.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); ck=vJYE; __utma=30149280.154571472.1568124005.1568300945.1568340826.5; __utmc=30149280; __utma=81379588.1910030307.1568124005.1568300945.1568340826.4; __utmc=81379588; ap_v=0,6.0; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1568343917%2C%22https%3A%2F%2Fwww.baidu.com%2Fs%3Fwd%3D%25E8%25B1%2586%25E7%2593%25A3%26rsv_spt%3D1%26rsv_iqid%3D0xe5249f3f00029890%26issp%3D1%26f%3D8%26rsv_bp%3D1%26rsv_idx%3D2%26ie%3Dutf-8%26rqlang%3Dcn%26tn%3Dbaiduhome_pg%26rsv_enter%3D1%26rsv_dl%3Dtb%26oq%3Dmac%2525E5%2525AE%252589%2525E8%2525A3%252585vscode%26inputT%3D3660%26rsv_t%3D836erG0wNVO2v8Lp4CwMQ0OT2lRohicLTEcxqL9x7D%252BSWtZMjzqaZcTbRlUvz9eVtWVf%26rsv_pq%3De41b1e2c000246fa%26rsv_sug3%3D48%26rsv_sug1%3D38%26rsv_sug7%3D100%26rsv_sug2%3D0%26rsv_sug4%3D4368%22%5D; _pk_id.100001.3ac3=be5db9c252694557.1568124005.5.1568343917.1568340826.; _pk_ses.100001.3ac3=*'
	for i in cookies.split(';'):
		dic_c[i.split('=')[0]] = i.split('=')[1]
# 获取数据信息页面网址
	datalst = []
	for u in urllst1:
		try:
			datalst.extend(get_data(u,dic_h,dic_h))
			print('成功采集第%i条数据'%len(datalst))
		except:
			print('页面访问失败，网址为',u)

	datadf = pd.DataFrame(datalst)
	datadf['评分'] = datadf['评价'].str.split('(').str[0]
	datadf['评论人数'] = datadf['评价'].str.split('(').str[1].str.split('人').str[0]
	# datadf['评分'] = datadf[datadf['评价'] != "(少于10人评价)"]['评分'].astype('float')
	datadf['评论人数'] = datadf[datadf['评价'] != "(少于10人评价)"]['评论人数'].astype('int')

