# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 14:02:00 2017

@author: ThinkPad
"""

import requests
from bs4 import BeautifulSoup
import pymysql
import pymysql.cursors
import time

def get_house_cards(headers,url):
	resp = requests.get(url,headers).content
	soup = BeautifulSoup(resp, 'lxml')
	house_list = soup.find_all('div', attrs={'class':'info'})
	return house_list

def create_mysql_table(dbname,tablename):
	conn = pymysql.connect(host='localhost',
						port = 3306,
						user = 'root',
						password = 	'12345678',
						db = dbname,
						charset='UTF8')
	cur = conn.cursor()
	Colnames = ['房屋链接','小区名称','房产交通','成交总价','均价','成交时间','房屋户型','所在楼层','建筑面积','户型结构','套内面积','建筑类型',
	'房屋朝向','建成年代','装修情况','梯户比例','产权年限']
	Colname = ''
	ColStyle = ' VARCHAR(100)'
	for i in Colnames:
		Colname = Colname+' '+i+ColStyle+','
	cur.execute("DROP TABLE IF EXISTS %s"%tablename)
	cur.execute("CREATE TABLE IF NOT EXISTS %s (%s)"%(tablename,Colname[:-1]))
	print('表-%s 创建成功！'%tablename)
	return cur,conn
	
def get_house_detail_info(url):
	print('正在房屋详细信息...')
	resp = requests.get(url).content
	soup =BeautifulSoup(resp, 'lxml')
	house_div = soup.find('div', attrs={'class':'content'})
	lis = house_div.find_all('li')
	values = []
	for li in lis:
		key = li.find('span').getText().strip()
		all_str = li.getText()
		value = all_str.strip(key).strip()
		if key in ['房屋户型','所在楼层','建筑面积','户型结构','套内面积','建筑类型',
		'房屋朝向','建成年代','装修情况','梯户比例','产权年限']:
			values.append(value)
	return values

def get_house_basic_info(div):
	print('正在获取房屋信息...')
	basic_values = []
	title = div.find('div', attrs={'class':'title'}).getText()
	link = div.find('div', attrs={'class':'title'}).find('a')['href']
	try:
		dealhouse_spans = div.find('span', attrs={'class':'dealHouseTxt'}).find_all('span')
		if len(dealhouse_spans) == 1:
			dealhouse = dealhouse_spans[0].getText()
		else:
			split_str = '/'
			dealhouse = dealhouse_spans[0].getText()+split_str+dealhouse_spans[1].getText()
			
	except:
		dealhouse = '暂无数据'
	total_price = div.find('div', attrs={'class':'totalPrice'}).getText().strip()
	unit_price = div.find('div', attrs={'class':'unitPrice'}).getText().strip()
	deal_date = div.find('div', attrs={'class':'dealDate'}).getText().strip()
	basic_values = [link, title, dealhouse, total_price, unit_price,deal_date]
	return basic_values

def save_to_mysql(cur,conn,data,TableName):
	Row = ''
	for i in data:
		Row = (Row+'"%s"'+',')%i
	print(Row)
	cur.execute("INSERT INTO %s VALUES (%s)"%(TableName,Row[:-1]))
	conn.commit()
	print('成功存入数据库！')
	
def main():
	n = 100
	init_url = 'https://nj.lianjia.com/chengjiao/pg'
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
			}
	print('正在连接数据库...')
	cur,conn = create_mysql_table('lianjia','house_records')
	for i in range(1,n+1):
		if i/10 == 0:
			time.sleep(5)
		else:
			url = init_url + str(i) + '/'
			print('正在获取第%s页信息......'%i)
			house_list = get_house_cards(headers,url)
			for house in house_list:
				value1 = get_house_basic_info(house)
				url = value1[0]
				value2 = get_house_detail_info(url)
				values = value1+value2
				save_to_mysql(cur, conn,values, 'house_records')
				print('-----------------------------')
			print('==============================')
	cur.close()
	conn.close()
		
if __name__ == '__main__':
	main()
			
			