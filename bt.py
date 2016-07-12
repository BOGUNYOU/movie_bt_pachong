#!usr/bin/python
# _*_ coding:utf-8 _*_

import urllib2
import cookielib
import bs4
import re
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def get_movie(url):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9',
	    'Connection':'keep-alive',
	    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	    'Cache-Control':'max-age=0'
	}

    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    request = urllib2.Request(url = url,headers = headers)
    response = urllib2.urlopen(request)
    contents = response.read()
    content = bs4.BeautifulSoup(contents,'html.parser')

    return content
def get_url(url):
	get_url_num_content = get_movie(url)
	get_url_num = get_url_num_content.find_all(name = 'span',class_ = 'pageinfo')
	get_num = get_url_num[0].strong.string
	total_url = []
	for i in range(int(get_num)):
		complete_url = url + "/?PageNo=" + str(i+1)
		total_url.append(complete_url)
	return total_url

def get_all_name(url):
	movie_name = get_movie(url)
	count = movie_name.find_all(name = 'p',class_ = 'tt cl')
	return count
def get_single_name(url):
	single_name = get_all_name(url)
	num = single_name.__len__()
	s_list = []
	for i in range(num):
		s = single_name[i].b
		s_sum = s.contents
		s_list.append(s_sum)
	return s_list
def get_movie_name(url):
	one_name = get_single_name(url)
	name_list = []
	for i in range(one_name.__len__()):
		if one_name[i].__len__() == 1:
			name_test = one_name[i][0]
			try:
				name = name_test.contents[0]
			except:
				name = name_test

		else:
			name = one_name[i][0]
		name_list.append(name)
	return name_list
def get_douban_goals(url):
	db_goal = get_movie(url)
	single_db_goal = db_goal.find_all(name = 'p',class_ = 'rt')
	goal_num = single_db_goal.__len__()
	goal_list = []
	for i in range(goal_num):
		try:
			int_goal = single_db_goal[i].strong.string
			point_goal = single_db_goal[i].find_all(name = 'em',class_ = 'fm')[0].string
			integrated_goal = int(int_goal) + float(point_goal)/10
			goal_list.append(integrated_goal)
		except:
			pass
	return goal_list

def combination_name_goal(url):
	e = get_movie_name(url)
	f = get_douban_goals(url)
	d = {}	
	for i in range(e.__len__()):
		d[e[i]] = f[i]
	reverse_goal = sorted(d.iteritems(),key = lambda d:d[1],reverse = True)
	return reverse_goal

def save_name(url):
	c = get_movie_name(url)
	w = get_douban_goals(url)
	conn = MySQLdb.connect(host = 'localhost',user = 'root',charset = 'utf8')
	cui = conn.cursor()
	cui.execute("""create database if not exists bt_sql """)
	conn.select_db("bt_sql")
	cui.execute("""create table if not exists tet(name varchar(30),goal float) """)
	try:
		for i in range(c.__len__()):
			z = [c[i],w[i]]
			cui.execute("insert into tet(name,goal) value(%s,%s)",z)
	except:
		pass
	conn.commit()
	conn.close()




URL = 'http://www.bttiantang.com'
o = get_url(URL)
#s = "豆瓣评分：".decode("utf-8").encode("GBK")
#dot = u'\u2027'
page = int(0)
for i in range(o.__len__()):
	page = page + 1
	print page
	single_page_url = o[i]
	f = combination_name_goal(single_page_url)
	l = save_name(single_page_url)
#	for i in range(f.__len__()):
#		n = f[i][1]
#		try:
#			m = f[i][0].encode("GBK")
#			print "%-30s%s%.1f" % (m,s,n)
#		except:
#			continue
