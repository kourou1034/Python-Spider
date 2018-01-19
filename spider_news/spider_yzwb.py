# -*- coding: UTF-8 -*-
# 扬子晚报
import requests
from bs4 import BeautifulSoup
import time
import codecs
import json

def get_article_url(url ,headers):
    req = requests.get(url,headers)
    data = req.text
    soup = BeautifulSoup(data,'lxml')
    article_list = soup.find('div',attrs={'class':'main-left left white'}).find_all('div',attrs={'class':'box'})
    urls = []
    for article in article_list:
        article_time = article.find('div',attrs={'class':'box-text-time'}).find('span').getText()
        month = int(article_time[5:7])
        day = int(article_time[8:10])
        now_month = int(time.localtime(time.time())[1])
        now_day = int(time.localtime(time.time())[2])
        if day == now_day and month == now_month:
            article_url = article.find('div',attrs={'class':'box-text-title'}).find('a')['href']
            urls.append(article_url)
    return urls


def get_article(url, headers, count):
    print(url)
    req = requests.get(url,headers)
    data = req.text
    soup = BeautifulSoup(data,'lxml')
    article = soup.find('div',attrs={'class':'news-main-banner'})
    article_title = article.find('div',attrs={'class':'text-title'}).getText().strip()
    article_time = article.find('div',attrs={'class':'text-time'}).getText()[-19:-9]
    folder = article_time+'yzwb%s.txt'%count
    fp = codecs.open('data/article.csv', 'a+', 'utf-8')
    fp.write(article_title+','+article_time+','+url+','+folder+'\r\n')
    fp.close()
    body = article.find('div',attrs={'class':'text-text'}).find_all('p')
    for b in body:
        text = b.getText()
        fp1 = codecs.open('articles/'+folder, 'a+', 'utf-8')
        fp1.write(text+'\r\n')
        fp1.close()


def main():
    init_url = ['http://www.yangtse.com/app/jiangsu/kanjiangsu/index.html',
        'http://www.yangtse.com/app/jiangsu/kanjiangsu/index_2.html',
        'http://www.yangtse.com/app/jiangsu/kanjiangsu/index_3.html'
        ]
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Host':'news.jstv.com',
    }
    count = 1
    for url in init_url:
        urls = get_article_url(url, headers)
        for u in urls:
            try:
                get_article(u, headers, count)
                count += 1
                fp = codecs.open('data/log.txt','a+', 'utf-8')
                fp.write('Succeed.  '+u+'\r\n')
                fp.close()
            except:
                fp = codecs.open('data/log.txt','a+', 'utf-8')
                fp.write('Failed.  '+u+'\r\n')
                fp.close()

if __name__ == '__main__':
    main()