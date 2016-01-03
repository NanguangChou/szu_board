#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import urllib
import urllib2
from mysqlhelper import MySQL
from pyquery import PyQuery as pq
import cookielib


def main():
	#数据库连接参数  
	dbconfig = {'host':'hostname', 
		'port': 3306, 
		'user':'root', 
		'passwd':'username', 
		'db':'szu', 
		'charset':'utf8'}

	# db = MySQL(dbconfig)
	# sql = 'select * from `board`'
	# db.query(sql)

	# result = db.fetchAllRows()
	# for row in result:
	# 	for colum in row:
	# 		print colum
	# db.close()
	url = 'http://www.szu.edu.cn/board/'
	# value = {
	# 		'search_type':'title',
	# 		'dayy':'365#一年',
	# 		'keyword':'1',
	# 		'searchb1':'搜索',
	# }
	# data = urllib.urlencode(value)
	# 坑爹的gbk编码
	# data = 'dayy=365%23%D2%BB%C4%EA&search_type=title&keyword=&keyword_user=&searchb1=%CB%D1%CB%F7'
	# print data;
	result = easy_curl(url)
	result = result.read()
	dollar = pq(result)
	mes_list =  dollar('.tbcolor13').parent().children()
	for i in range(2,mes_list.length):
		ele = mes_list.eq(i)
		insertdata = {}
		insertdata['title'] = ele.find('td').eq(3).find('a').text()
		print insertdata['title']
def easy_curl(url,data=''):
	send_headers = {
		'Host':'www.szu.edu.cn',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Connection':'keep-alive'
	}
	cookie = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
	response = opener.open('http://192.168.2.20/')
	req = urllib2.Request(url,headers=send_headers,data=data)
	r = urllib2.urlopen(req)
	return r
#
if __name__ == '__main__':
	main()