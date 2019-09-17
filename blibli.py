import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import pymongo

def get_urls(u,d_h,d_c):
	'''
	视频页面url采集
	:param n: 起始页面
	:param d_h: user-agent信息
	:param d_ c: cookies信息
	:return: 得到一个视频页面的list
	'''
	ri = requests.get(url = u ,headers = d_h,cookies = d_c)
	soupi = BeautifulSoup(ri.text,'lxml')
	lis = soupi.find('ul',class_ ="video-list clearfix").find_all('li')
	lst = []
	for i in lis:
		lst.append('http:' + i.a['href'])
	return lst

def get_data(ui,d_h,d_c,table):
	'''
	视频页面数据采集/cid信息/弹幕xml数据采集
	:param ui:
	:param d_h:
	:param d_c:
	:return:
	'''

	ri = requests.get(url = ui ,headers = d_h,cookies = d_c)
	soup1 = BeautifulSoup(ri.text,'lxml')
	name = soup1.h1['title']
	time = re.search(r'(20.*:\d{2})',soup1.find('div' ,class_="video-data").text).group(1)
	cid = re.search(r'"cid":(\d*),',ri.text).group(1)

	cid_url = 'http://comment.bilibili.com/{}.xml' .format(cid)
	r2 = requests.get(url = cid_url,headers = d_h,cookies = d_c)

	soup2  = BeautifulSoup(r2.text,'lxml')
	r2.encoding = r2.apparent_encoding
	dmlst = re.findall(r'<d.*?/d>',r2.text)
	n = 0
	for dm in dmlst:
		dic = {}
		dic['标题'] = name
		dic['发布时间'] = time
		dic['cid'] = cid
		dic['弹幕内容'] = re.search(r'>(.*)<',dm).group(1)
		dic['其他信息'] = re.search(r'p="(.*)">',dm).group(1)
		table.insert_one(dic)
		n += 1
	return n


if __name__ == "__main__":
	dic_h = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
	cookies = "_uuid=4AC4494C-AA71-6EAD-80E8-EE81EA3569A441102infoc; buvid3=4A6ECF65-262E-42B7-B8D5-4B31499647DF155818infoc; LIVE_BUVID=AUTO3515664811422634; sid=cofm687y; DedeUserID=29266481; DedeUserID__ckMd5=7709f6eacd9f36a8; SESSDATA=c604d1af%2C1569073276%2C28d68f81; bili_jct=3e7703db51c9ff397a3785e896f4a695; fts=1566481323; CURRENT_FNVAL=16; rpdid=|(u)~lJY||Ym0J'ulYYR)uJRJ; stardustvideo=1; CURRENT_QUALITY=80; arrange=matrix"
	dic_c = {}
	for i in cookies.split(';'):
		dic_c[i.split('=')[0]] = i.split('=')[1]
		#获取headers,cookies
	u1 = 'https://search.bilibili.com/video?keyword=%E9%BB%84%E6%99%93%E6%98%8E'

	urllst = get_urls(u1,dic_h,dic_c)


	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	db = myclient['blibli']
	datatable = db['data2']

	errotlst = []
	count = 0
	for u in urllst:
		try:
			count += get_data(u,dic_h,dic_c,datatable)
			print('数据采集成功，总共采集%i条数据' % count)
		except:
			errotlst.append(u)
			print('数据采集失败，网址为',u)
