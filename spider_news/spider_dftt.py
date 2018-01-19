# -*- coding: UTF-8 -*-
# 东方头条
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import json
import codecs
import time


def get_article_url(url,headers):
    req = requests.get(url,headers=headers)
    data = req.content
    soup = BeautifulSoup(data,'lxml')
    article_div = soup.find('div',attrs={'id':'J_hot_news'})
    list_top = article_div.find('div',attrs={'class':'hot-news-top'}).find_all('li')
    list_bottom = article_div.find('div',attrs={'class':'hot-news-bottom'}).find_all('li')
    list_top.extend(list_bottom)
    article_list = list_top
    urls = []
    for li in article_list:
        a = li.find_all('a')
        for i in a:
            article_url = 'http:' + i['href']
            urls.append(article_url)
    return urls


def get_article(url,headers, count):
    req = requests.get(url, headers)
    data = req.content
    soup = BeautifulSoup(data,'lxml')
    title = soup.find('div',attrs={'class':'detail_left_cnt'}).find('div',attrs={'class':'J-title_detail title_detail'}).find('h1').getText().strip()
    article_time = soup.find('div',attrs={'class':'detail_left_cnt'}).find('div',attrs={'class':'J-title_detail title_detail'}).find('div',attrs={'class':'fl'}).find('i').getText().strip()[0:10]
    body = soup.find('div',attrs={'class':'detail_left_cnt'}).find('div',attrs={'class':'J-contain_detail_cnt contain_detail_cnt'}).find_all('p')
    folder = article_time+'dftt%s.txt'%count
    fp = codecs.open('data/article.csv','a+', 'utf-8')
    fp.write(title+','+article_time+','+url+','+folder+'\r\n')
    fp.close()
    fp = codecs.open('articles/'+folder, 'a+', 'utf-8')
    for b in body:
        text = b.getText()
        fp.write(text+'\r\n')
    fp.close()

def main():
    init_url = 'http://mini.eastday.com/'
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'*/*'
        }
    urls = get_article_url(init_url,headers)
    count = 0
    for url in urls:
        try:
            count += 1
            get_article(url,headers,count)
            fp = codecs.open('data/log.txt','a+', 'utf-8')
            fp.write('Succeed.  '+url+'\r\n')
            fp.close()
        except:
            fp = codecs.open('data/log.txt','a+', 'utf-8')
            fp.write('Failed.  '+url+'\r\n')
            fp.close()

if __name__ == '__main__':
    main()