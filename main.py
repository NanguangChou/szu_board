#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import urllib
import urllib2
from mysqlhelper import MySQL
from pyquery import PyQuery as pq
import cookielib
import re
import time

debug = True

def setLog(log_message):
	log_filename = '/tmp/szu_board.log'
	logger=logging.getLogger()
	handler=logging.FileHandler(log_filename)
	logger.addHandler(handler)
	logger.setLevel(logging.INFO)
	logger.debug(log_message)
	# 如果没有此句话，则会将同一个message追加到不同的log中
	logger.removeHandler(handler)

def strQ2B(ustring):
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:         
            inside_code = 32 
        elif (inside_code >= 65281 and inside_code <= 65374):
            inside_code -= 65248

        rstring += unichr(inside_code)
    return rstring



def main():
	#数据库连接参数  
	dbconfig = {'host':'localhost', 
		'port': 3306, 
		'user':'root', 
		'passwd':'', 
		'db':'szu1983', 
		'charset':'utf8'
	}
	if not(debug):
		db = MySQL(dbconfig)
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
	k=0;
	for i in range(2,10):#mes_list.length):#):
		ele = mes_list.eq(i).find('td')
		insertdata = {}
		insertdata['category'] = ele.eq(1).text()
		insertdata['title'] = ele.eq(3).find('a').text()
		toptext = ele.eq(3).find('font').text()
		insertdata['top'] = bool(toptext[0:4]==u'|置顶|') and 1 or 0
		print insertdata['top']
		inner_link = ele.eq(3).find('a').attr('href')
		if not(inner_link):
			continue
		insertdata['id'] = inner_link[-6:]
		inner_link = url+inner_link
		content = easy_curl(inner_link).read()
		inner_dollar = pq(content)
		inner_ele = inner_dollar('.fontcolor3').eq(1)
		temp = inner_ele.find('font').eq(0).text().split(' ')
		if(len(temp)>1 and temp[0]!=temp[1]):
			title = temp[0]+temp[1]
		else:
			title = temp[0] 
		insertdata['title'] = title
		#存日期和发文单位
		pattern = re.compile(r'\<font color=#808080\>(.*)\<\/font\>')
		result = pattern.findall(content)
		print result[0].decode('gbk').encode('utf-8')
		author_date = result[0].decode('gbk')

		author_date = strQ2B(author_date).split(' ')

		date_str    = author_date[1]+' '+author_date[2]
		date        = int(time.mktime(time.strptime(date_str,'%Y-%m-%d %H:%M:%S')))
		insertdata['date'] = date
		insertdata['author'] = author_date[0]
		#存附件
		files       = []
		files_eles  = inner_ele.parent().next().next().next().find('a')
		for j in files_eles:
			files.append(pq(j).attr('href'))
		insertdata['attachments'] = files
		#存最后更新时间
		update_str    = inner_ele.parent().next().next().next().find('tr').children().eq(1).text()
		if not(update_str):
			insertdata['lastEdit'] = date
		else:
			update_str = strQ2B(update_str[4:25]).split(' ')
			lastEdit   = update_str[0]+' '+update_str[1]
			lastEdit   = int(time.mktime(time.strptime(lastEdit,'%Y-%m-%d %H:%M:%S')))
			insertdata['lastEdit'] = lastEdit

		new_dom   =  inner_ele.parent().next().next().children().eq(0)
		clean_dom =  new_dom.find('*')
		for item in clean_dom:
			pq(item).attr('style','')
			pq(item).attr('class','')
		insertdata['content'] = (new_dom.html())
		id = insertdata['id']
		category = insertdata['category']
		lastEdit = insertdata['lastEdit']
		fujian = insertdata['attachments']
		attachments = '['
		for i in range(0,len(fujian)):
			attachments = attachments +'"'+ fujian[i]+'"'
		attachments = attachments+']'
		# print attachments
		insertdata['attachments'] = attachments
		date = insertdata['date']
		author = insertdata['author']
		title = insertdata['title']
		top = insertdata['top']
		content = insertdata['content']
		# print str(content)
		if not(debug):

			sql = 'delete from `board` where `id`='+id
			db.query(sql)
			db.insert('board', insertdata)
			# print sql2
			# db.query(sql2)
			print insertdata['title']
			k= k+1;
			print 'sql query '+str(k)+' succeed'

		else: 
			del insertdata['content']
			for item in insertdata:
				print insertdata[item]
		
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