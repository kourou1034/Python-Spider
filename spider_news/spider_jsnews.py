# -*- coding: UTF-8 -*-
# 中国江苏网-新闻
import requests
from bs4 import BeautifulSoup
import time
import json
import codecs


def get_article_url(url, headers):
    req = requests.get(url,headers=headers)
    data = req.text
    fp = codecs.open('test/error.txt','a+', 'utf-8')
    fp.write(data)
    fp.close()
    soup = BeautifulSoup(data,'lxml')
    article_list = soup.find_all('div',attrs={'class':'biaot'})
    urls = []
    for article in article_list:
        article_time = article.find('span').getText()[:10]
        day = int(article_time[8:10])
        month = int(article_time[5:7])
        now_month = int(time.localtime(time.time())[1])
        now_day = int(time.localtime(time.time())[2])
        if day == now_day and month == now_month:
            article_url = 'http://jsnews.jschina.com.cn/jsyw/'+article.find('a')['href'][1:]
            urls.append(article_url)
        else:
            break
    return urls

def get_article(url, headers,count):
    req = requests.get(url, headers=headers)
    data = req.content
    soup = BeautifulSoup(data,'lxml')
    title = soup.find('div',attrs={'class':'text'}).find('h2').getText()
    article_time = soup.find('div',attrs={'class':'text'}).find('div',attrs={'class':'info'}).find('span',attrs={'id':'pubtime_baidu'}).getText()[:10]
    body = soup.find('div',attrs={'class':'article'}).find_all('p')
    folder = article_time+'jsxww%s.txt'%count
    fp = codecs.open('data/article.csv','a+', 'utf-8')
    fp.write(title+','+article_time+','+url+','+folder+'\r\n')
    fp.close()
    fp = codecs.open('articles/'+folder, 'a+', 'utf-8')
    for b in body:
        text = b.getText()
        fp.write(text+'\r\n')
    fp.close()


def main():
    init_url = ['http://jsnews.jschina.com.cn/jsyw/index.shtml',
        'http://jsnews.jschina.com.cn/jsyw/index_1.shtml']
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        }
    count = 1
    for url in init_url:
        urls = get_article_url(url,headers)
        for u in urls:
            try:
                get_article(u,headers,count)
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