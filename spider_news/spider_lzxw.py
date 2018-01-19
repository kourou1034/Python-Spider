# -*- coding: UTF-8 -*-
# 荔枝新闻
import requests
from bs4 import BeautifulSoup
import json
import codecs
import time

def get_article_url(url,headers):
    req = requests.get(url,headers=headers)
    data = req.text
    data = data[10:-2]+']'
    fp = codecs.open('test.txt','w','utf-8')
    fp.write(data)
    fp.close()
    article_lsit = json.loads(data)
    urls = []
    titles = []
    for article in article_lsit:
        article_url = article['linkHref']
        article_title = article['title']
        titles.append(article_title)
        urls.append(article_url)
    return urls,titles


def get_article(url,headers,count,title):
    req = requests.get(url, headers=headers)
    data = req.content
    soup = BeautifulSoup(data,'lxml')
    article_time = soup.find('div', attrs={'class':'article'}).find('span',attrs={'class':'time'}).getText().strip()[:10]
    month = int(article_time[5:7])
    day = int(article_time[8:10])
    now_month = int(time.localtime(time.time())[1])
    now_day = int(time.localtime(time.time())[2])
    if day == now_day and month == now_month:
        article_time = article_time[0:4]+'-'+str(month)+'-'+str(day)
        body = soup.find('div',attrs={'class':'article'}).find('div',attrs={'class':'content'}).find_all('p')
        folder = article_time+'lzxw%s.txt'%count
        fp = codecs.open('data/article.csv','a+','utf-8')
        fp.write(title+','+article_time+','+url+','+folder+'\r\n')
        fp.close()
        fp1 = codecs.open('articles/'+folder, 'a+', 'utf-8')
        for b in body:
            text = b.getText()
            fp1.write(text+'\r\n')
        fp1.close()

def main():
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        }
    init_url = ['http://news.jstv.com/app/s/app_list.js?_=%s'%(str(int(time.time())-1)+'123')]
    for i in range(2,6):
        url1 = 'http://news.jstv.com/app/s/app_list_'+str(i)+'.js?_=%s'%(str(int(time.time())-1)+'123')
        init_url.append(url1)
    count = 1
    status = 1
    for url in init_url:
        if status == 0:
            break
        urls,titles = get_article_url(url,headers)
        for j in range(len(urls)):
            try:
                print(urls[j])
                status = get_article(urls[j],headers,count,titles[j])
                count += 1
                fp = codecs.open('data/log.txt','a+', 'utf-8')
                fp.write('Succeed.  '+urls[j]+'\r\n')
                fp.close()
                if status == 0:
                    break
            except:
                fp = codecs.open('data/log.txt','a+', 'utf-8')
                fp.write('Failed.  '+urls[j]+'\r\n')
                fp.close()



if __name__ == '__main__':
    main()