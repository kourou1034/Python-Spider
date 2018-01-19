# -*- coding: UTF-8 -*-
# 新华报业江苏
import requests
from bs4 import BeautifulSoup
import time
import json
import codecs

def get_article_url(url,headers):
    req = requests.get(url,headers=headers)
    data = req.content
    soup = BeautifulSoup(data,'lxml')
    divs = soup.find('div',attrs={'id':'jsleft'}).find_all('div',attrs={'id':'jsl_dh'})
    urls = []
    for div in divs:
        lis = div.find_all('li')
        for li in lis:
            title = li.find('a').getText()
            text = li.getText()
            article_time = text.replace(title,'').strip()
            month = int(article_time[5:7])
            day = int(article_time[8:10])
            now_month = int(time.localtime(time.time())[1])
            now_day = int(time.localtime(time.time())[2])
            if day == now_day and month == now_month:
                article_url = li.find('a')['href']
                urls.append(article_url)
    return urls


def get_article(url,headers,count):
    req = requests.get(url,headers=headers)
    data = req.content
    soup = BeautifulSoup(data,'lxml')
    article_text = soup.find('div',attrs={'class':'text'})
    article_title = article_text.find('h2').getText()
    article_time = article_text.find('span',attrs={'id':'pubtime_baidu'}).getText()[:10]
    folder = article_time + 'xhby%s.txt'%count
    fp = codecs.open('data/article.csv','a+','utf-8')
    fp.write(article_title+','+article_time+','+url+','+folder+'\r\n')
    fp.close()
    body = article_text.find('div',attrs={'class':'article'}).find_all('p')
    fp1 = codecs.open('articles/'+folder, 'a+','utf-8')
    for b in body:
        text = b.getText()
        fp1.write(text+'\r\n')
    fp1.close()



def main():
    init_url = 'http://js.xhby.net/'
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
            fp = codecs.open('data/log.txt','a+', 'utf-8')
            fp.write('Failed.'+'\t'+u+'\t'+e.message+'\r\n')
            fp.close()


if __name__ == '__main__':
    main()