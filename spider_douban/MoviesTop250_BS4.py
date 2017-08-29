# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 14:54:16 2017

@author: ThinkPad
"""
# requests库+BeaytifulSoup爬取豆瓣电影top250
import requests
from bs4 import BeautifulSoup

class MoviesTop250:
    def __init__ (self):
        
        self.Geturl = 'https://movie.douban.com/top250'
        self.headers = {
                'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
                                          }
        self.SavePath = './movies250.txt'
        
    def get_page(self, url):
        data = requests.get(url, headers=self.headers).content
        return data
    
    def parser_html(self, url):
        html = self.get_page(url)
        soup = BeautifulSoup(html, 'lxml')
        movie_list_soup = soup.find('ol', attrs = {'class':'grid_view'})
        movie_name_list = []
        for movie_li in movie_list_soup.find_all('li'):
            try:
                num = movie_li.find('em', attrs={'class':''}).getText()
                detail = movie_li.find('div', attrs = {'class':'hd'})
                movie_name = detail.find_all('span', attrs = {'class':'title'})
                name1 = movie_name[0].getText()
                info = movie_li.find('p', attrs={'class':""}).getText()
                rating_num = movie_li.find('span', attrs={'class':'rating_num'}).getText()
                inq = movie_li.find('span', attrs={'class':'inq'}).get_text()
            except:
                continue
            if len(movie_name) == 2:
                name2 = movie_name[1].getText()
            else:
                name2 = 'none'
            movie_name_list.append([num, name1, name2, info, rating_num, inq])
        next_page = soup.find('span', attrs = {'class':'next'}).find('a')
        if next_page:
            return movie_name_list, self.Geturl + next_page['href']
            
        return movie_name_list, None
    
    def WriteMovies(self):
        URL = self.Geturl
        fp = open(self.SavePath, 'w', encoding='utf-8')
        n = 1
        while URL:
            print('正在抓取%d-%d部电影...' %(n, n+24))
            movies, URL = self.parser_html(URL)
            n += 24
            print('正在写入...')
            for movie in movies:
                fp.write('电影排名: ' + movie[0] + '\r\n')
                fp.write('电影名称: ' + movie[1] + movie[2].replace(' ','') + '\r\n')
                fp.write('电影简介: ' + movie[3].replace(' ','').replace('\n', ' ') + '\r\n')
                fp.write('电影评分: ' + movie[4] + '\r\n')
                fp.write('一句简评: ' + movie[5] + '\r\n\r\n')
             
    def main(self):
        print('正在从豆瓣电影Top250抓取数据...')
        # self.parser_html(URL)
        self.WriteMovies()
        print('抓取完毕,文件已保存！')
        
            
if __name__ == '__main__':
    MovieSpiser = MoviesTop250()
    MovieSpiser.main()
            
