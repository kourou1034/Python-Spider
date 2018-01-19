# -*- coding: UTF-8 -*-
# 人民网江苏
import requests
from bs4 import BeautifulSoup
import time
import json
import codecs

def get_article_url(url,headers):
    req = requests.get(url, headers=headers)
    data = req.text
    fp = codecs.open('test.txt', 'w','utf-8')
    fp.write(data)
    fp.close()
    soup = BeautifulSoup(data,'lxml')
    uls = soup.find('div',attrs={'class':'ej_list_box clear'}).find_all('ul')
    urls = []
    for ul in uls:
        lis = ul.find_all('li')
        for li in lis:
            article_time = li.find('em').getText()
            month = int(article_time[5:7])
            day = int(article_time[8:10])
            now_month = int(time.localtime(time.time())[1])
            now_day = int(time.localtime(time.time())[2])
            if day == now_day and month == now_month:
                article_url = 'http://js.people.com.cn'+li.find('a')['href']
                urls.append(article_url)
    return urls


def get_article(url,headers,count):
    req = requests.get(url, headers=headers)
    data = req.content
    soup = BeautifulSoup(data,'lxml')
    article_title = soup.find('div',attrs={'class':'clearfix w1000_320 text_title'}).find('h1').getText()
    article_time = soup.find('div',attrs={'class':'clearfix w1000_320 text_title'}).find('div',attrs={'class':'box01'}).find('div',attrs={'class':'fl'}).getText().strip()
    article_time = article_time[0:4]+'-'+article_time[5:7]+'-'+article_time[8:10]
    folder = article_time+'rmwjs%s.txt'%count
    fp = codecs.open('data/article.csv','a+', 'utf-8')
    fp.write(article_title+','+article_time+','+url+','+folder+'\r\n')
    fp.close()
    body = soup.find('div',attrs={'class':'clearfix w1000_320 text_con'}).find('div',attrs={'class':'box_con'}).find_all('p')
    fp1 = codecs.open('articles/'+folder, 'a+', 'utf-8')
    for b in body:
        text = b.getText()
        fp1.write(text+'\r\n')
    fp1.close()




def main():
    init_url = 'http://js.people.com.cn/GB/360297/index.html'
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        }
    urls = get_article_url(init_url, headers)
    count = 1
    for u in urls:
        try:
            get_article(u, headers, count)
            count += 1
            fp = codecs.open('data/log.txt','a+', 'utf-8')
            fp.write('Succeed.  '+u+'\r\n')
            fp.close()
        except Exception as e:
            print e.message
            fp = codecs.open('data/log.txt','a+', 'utf-8')
            fp.write('Failed.'+'\t'+u+'\t'+e.message+'\r\n')
            fp.close()


if __name__ == '__main__':
    main()