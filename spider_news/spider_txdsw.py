# -*- coding: UTF-8 -*-
# 腾讯大苏网
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
    soup = BeautifulSoup(data,'lxml')
    article_list = soup.find_all('ul',attrs={'class':'list01 font_s_14 line_h_25'})
    urls = []
    for ul in article_list:
        lis = ul.find_all('li')
        for li in lis:
            article_time = li.find('span').getText().strip()[:6]
            month = int(article_time[0:2])
            day = int(article_time[3:5])
            now_month = int(time.localtime(time.time())[1])
            now_day = int(time.localtime(time.time())[2])
            if day == now_day and month == now_month:
                article_url = li.find('a')['href']
                urls.append(article_url)
                status = 1
            else:
                status = 0
                break
        if status == 1:
            continue
        else:
            break
    return urls

def get_article(url,headers, count):
    req = requests.get(url, headers)
    data = req.text
    soup = BeautifulSoup(data,'lxml')
    title = soup.find('div',attrs={'id':'C-Main-Article-QQ'}).find('div',attrs={'class':'hd'}).find('h1').getText().strip()
    article_time = soup.find('div',attrs={'id':'C-Main-Article-QQ'}).find('div',attrs={'class':'hd'}).find('span',attrs={'class':'article-time'}).getText().strip()[0:10]
    body = soup.find('div',attrs={'id':'C-Main-Article-QQ'}).find('div',attrs={'id':'Cnt-Main-Article-QQ'}).find_all('p')
    folder = article_time+'txdsw%s.txt'%count
    fp = codecs.open('data/article.csv','a+', 'utf-8')
    fp.write(title+','+article_time+','+url+','+folder+'\r\n')
    fp.close()
    fp = codecs.open('articles/'+folder, 'a+', 'utf-8')
    for b in body:
        text = b.getText()
        fp.write(text+'\r\n')
    fp.close()

def main():
    init_url = 'http://js.qq.com/l/news/zq/nj/roll.htm'
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'*/*'
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