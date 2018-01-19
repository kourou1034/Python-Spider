# -*- coding: UTF-8 -*-
# 江苏都市
import requests
from bs4 import BeautifulSoup
import time
import json
import codecs

def get_article_url(url,headers):
    req = requests.get(url, headers=headers)
    data = req.content
    soup = BeautifulSoup(data,'lxml')
    lis = soup.find('div',attrs={'class':'col-l-main w-650'}).find('ul',attrs={'class':'mode-txtlink c-lists'}).find_all('li')
    urls = []
    for li in lis:
        try:
            article_time = li.find('span',attrs={'class':'date'}).getText()
            month = int(article_time.split(u'月')[0])
            day = int(article_time.split(u'月')[1].split(u'日')[0])
            now_month = int(time.localtime(time.time())[1])
            now_day = int(time.localtime(time.time())[2])
            if day == now_day and month == now_month:
                article_url = li.find('a')['href']
                urls.append(article_url)
        except:
            continue
    return urls



def get_article(url,headers,count):
    req = requests.get(url,headers=headers)
    data = req.content
    soup = BeautifulSoup(data,'lxml')
    article = soup.find('div',attrs={'class':'col-l-main w-650'}).find('div',attrs={'class':'content-wrap bor-9fc padd-20'})
    article_title = article.find('h1').getText().strip()
    article_time = article.find('div',attrs={'class':'arti-atttibute'}).find_all('span')[1].getText()[:10]
    folder = article_time+'jsds%s.txt'%str(count)
    fp = codecs.open('data/article.csv','a+','utf-8')
    fp.write(article_title+','+article_time+','+url+','+folder+'\r\n')
    fp.close()
    body = article.find('div',attrs={'class':'cont-detail fs-small'}).find_all('p')
    fp = codecs.open('articles/'+folder,'a+','utf-8')
    for p in body:
        text = p.getText()
        fp.write(text+'\r\n')
    fp.close()


def main():
    init_url = 'http://news.jsdushi.cn/jsnews/1.shtml'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    urls = get_article_url(init_url, headers)
    count = 1
    for u in urls:
        try:
            get_article(u, headers, count)
            count += 1
            fp = codecs.open('data/log.txt','a+', 'utf-8')
            fp.write('Succeed.'+'\t'+u+'\r\n')
            fp.close()
        except Exception as e:
            fp = codecs.open('data/log.txt','a+', 'utf-8')
            fp.write('Failed.'+'\t'+u+'\t'+e.message+'\r\n')
            fp.close()


if __name__ == '__main__':
    main()