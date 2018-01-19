# -*- coding: UTF-8 -*-
# 新浪-新闻
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import json
import codecs
import time


def get_article_url(url, headers):
    req = requests.get(url,headers=headers)
    data = req.content
    data = data[19:-2]
    data = json.loads(data)['result']['data']
    article_list = data['list']
    urls = []
    for article in article_list:
        # article_id = article['id']
        # article_title = article['title']
        # article_url = article['URL']
        article_time = article['fpTime'][:5]
        month = int(article_time[:2])
        day = int(article_time[3:])
        now_month = int(time.localtime(time.time())[1])
        now_day = int(time.localtime(time.time())[2])
        if day == now_day and month == now_month:
            urls.append(article_url)
    return urls

def get_article(url,headers, count):
    req = requests.get(url,headers=headers)
    data = req.content
    soup = BeautifulSoup(data,'lxml')
    article_box = soup.find('div',attrs={'class':'article-box'})
    title = article_box.find('div',attrs={'class':'article-header clearfix'}).find('h1').getText()
    article_time = article_box.find('p',attrs={'class':'source-time'}).find('span').getText()[:10]
    folder = article_time[:10]+'sina%s.txt'%count
    fp = codecs.open('data/article.csv','a+', 'utf-8')
    fp.write(title+','+article_time+','+url+','+folder+'\r\n')
    fp.close()
    body = article_box.find('div', attrs={'class':'article-body main-body'}).find_all('p')
    fp = codecs.open('articles/'+folder, 'a+', 'utf-8')
    for b in body:
        text = b.getText()
        fp.write(text)
        fp.write('\r\n')
    fp.close

def main():
    url = [
        'http://interface.sina.cn/dfz/jx/news/index.d.html?callback=jsonp%s&page=1&ch=zhengwen&cid=69634'%(str(int(time.time())-1)+'123'),
        'http://interface.sina.cn/dfz/jx/news/index.d.html?callback=jsonp%s&page=1&ch=zhengwen&cid=69635'%(str(int(time.time())-1)+'123'),
        'http://interface.sina.cn/dfz/jx/news/index.d.html?callback=jsonp%s&page=1&ch=zhengwen&cid=69636'%(str(int(time.time())-1)+'123')
        ]
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'*/*',
        'Refer':'http://jiangsu.sina.com.cn/news/general/list.shtml'
        }
    count = 1
    for u in url:
        urls = get_article_url(u,headers)
        for url in urls:
            try:
                get_article(url, headers, count)
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