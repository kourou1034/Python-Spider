# -*- coding: UTF-8 -*-
# 网易江苏
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import json
import codecs
import time


def get_article_url(url,headers):
    req = requests.get(url,headers=headers)
    data = req.text
    data = data[15:-1]
    fp = codecs.open('test/error.txt','w', 'utf-8')
    fp.write(data)
    fp.close()
    print(type(data))
    data = json.loads(data)
    urls = []
    for article in data:
        article_time = article['time']
        article_url = article['docurl']
        day = int(article_time[3:5])
        month = int(article_time[0:2])
        now_month = int(time.localtime(time.time())[1])
        now_day = int(time.localtime(time.time())[2])
        if day == now_day and month == now_month:
            urls.append(article_url)
    return urls

def get_article(url,headers, count):
    req = requests.get(url, headers=headers)
    data = req.content
    soup = BeautifulSoup(data,'lxml')
    title = soup.find('div',attrs={'class':'post_content_main'}).find('h1').getText().strip()
    body = soup.find('div',attrs={'class':'post_content_main'}).find('div',attrs={'class':'post_text'}).find_all('p')
    article_time = soup.find('div',attrs={'class':'post_time_source'}).getText().strip()[0:10]
    folder = article_time+'wangyi%s.txt'%count
    fp = codecs.open('test/article.csv','a+', 'utf-8')
    fp.write(title+','+article_time+','+url+','+folder+'\r\n')
    fp.close()
    fp = codecs.open('test/'+folder, 'a+', 'utf-8')
    for b in body:
        text = b.getText()
        fp.write(text+'\r\n')
    fp.close()

def main():
    params = str(int(time.time())-1)+'123'
    init_url = 'http://bendi.news.163.com/jiangsu/special/04248H8U/njxxl.js?callback=data_callback&_='+params
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'*/*',
        }
    urls = get_article_url(init_url,headers)
    count = 1
    for url in urls:
        try:
            get_article(url,headers,count)
            count += 1
            fp = codecs.open('data/log.txt','a+', 'utf-8')
            fp.write('Succeed.  '+url+'\r\n')
            fp.close()
        except:
            fp = codecs.open('data/log.txt','a+', 'utf-8')
            fp.write('Failed.  '+url+'\r\n')
            fp.close()

if __name__ == '__main__':
    main()