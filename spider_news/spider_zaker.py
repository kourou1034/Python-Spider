# -*- coding: UTF-8 -*-
# zaker
import requests
from bs4 import BeautifulSoup
import time
import json
import codecs


def get_article_url(url,headers):
    req = requests.get(url,headers=headers)
    data = req.content
    data = json.loads(data)
    articles = data['data']['article']
    urls = []
    code = 1
    print(len(articles))
    for article in articles:
        date = article['marks'][1]
        if date == u'昨天' or date == u'前天':
            code = 0
            break
        else:
            article_url = 'http:' + article['href']
            urls.append(article_url)
    return urls,code


def get_article(url,headers,count):
    req = requests.get(url, headers=headers)
    data = req.content
    soup = BeautifulSoup(data,'lxml')
    article_title = soup.find('div',attrs={'class':'article_header'}).find('h1').getText()
    article_time = time.strftime("%Y-%m-%d", time.localtime())
    folder = article_time+'zaker%s.txt'%count
    fp = codecs.open('data/article.csv','a+', 'utf-8')
    fp.write(article_title+','+article_time+','+url+','+folder+'\r\n')
    fp.close()
    body = soup.find('div',attrs={'class':'article_content'}).find('div',attrs={'id':'content'}).find_all('p')
    fp = codecs.open('articles/'+folder,'a+','utf-8')
    for p in body:
        text = p.getText()
        fp.write(text+'\r\n')
    fp.close()


def main():
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    count = 1
    for i in range(4):
        init_url = 'http://www.myzaker.com/news/next_new.php?f=myzaker_com&url=http%3A%2F%2Fiphone.myzaker.com%2Fzaker%2Fblog2news.php%3Fapp_id%3D10169%26since_date%3D'+str(int(time.time())-1)+'%26nt%3D'+str(i)+'%26_appid%3Diphone%26top_tab_id%3D12183%26_version%3D6.5&_version=6.5'
        urls,code = get_article_url(init_url, headers)
        for url in urls:
            try:
                get_article(url, headers, count)
                count += 1
                fp = codecs.open('data/log.txt','a+', 'utf-8')
                fp.write('Succeed.  '+url+'\r\n')
                fp.close()
            except Exception as e:
                fp = codecs.open('data/log.txt','a+', 'utf-8')
                fp.write('Failed.'+'\t'+url+'\t'+e.message+'\r\n')
                fp.close()
        if code == 0:
            break

if __name__ == '__main__':
    main()