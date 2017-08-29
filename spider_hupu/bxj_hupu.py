# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 08:40:03 2017

@author: ThinkPad
"""

import requests
from bs4 import BeautifulSoup
import pymysql.cursors
import pymysql

def hupubxj():
    url_id = '/bbs/34'
    url_head = 'https://m.hupu.com'
    url = url_head + url_id
    titles = []
    headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
                                             }
    while url:
        data = requests.get(url, headers=headers).content
        soup = BeautifulSoup(data, 'html.parser')
        topic_lists = soup.find_all('li')
        print('爬取中...')
        print(url) 
        if soup.find('a', attrs = {'dace-node':'5050_nextpage'})['class'] == ['disabled']:
            url = None
        else:
            next_page = soup.find('a', attrs={'dace-node':'5050_nextpage'})['href']
            url = url_head + next_page
           
        for topic_list in topic_lists:
            try:
                topic_title = topic_list.find('h3').getText()
                print(topic_title)
                titles.append(topic_title)
            except:
                continue
    return titles

def create_table():
    print('==================爬取虎扑步行街贴子标题============================')
    titles = hupubxj()
    print('爬取成功，正在写入数据库...')
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='12345678',
                           db='hupu',
                           charset='UTF8')
    cur = conn.cursor()
    # cur.execute("drop table if exists topics_titles")
    cur.execute("create table if not exists topics_titles(name char(200))")
    for title in titles:
        cur.execute("insert into topics_titles(name) value ('%s')" %title)
    conn.commit()
    print('写入成功！')
    
    
if __name__ == '__main__':
    create_table()