# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 09:46:49 2017

@author: ThinkPad
"""

# -*- coding: utf-8 -*-
"""
Created on Sun May 14 15:45:57 2017

@author: ThinkPad
"""

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

def get_data(url, headers,ws):
    #song_list = []
    for i in range(40):
        n = 35*i
        urls = url + '&limit={sum}&offset={page}'.format(sum=35, page=n)
        print(urls)
        data = requests.get(urls, headers=headers).content
        soup = BeautifulSoup(data, 'lxml')
        playlists = soup.find_all('a', attrs={'class':'msk'})
        for lis in playlists:
            #play_dict = {'title':[], 'tag':[], 'music':[], 'url':[]}
            count = 0
            print("="*10 + lis['title'] + "="*10)
            new_url = 'http://music.163.com' + str(lis['href'])
            print(new_url)  
            music_data = requests.get(new_url, headers=headers).content
            music_soup = BeautifulSoup(music_data, 'lxml')
            musics = music_soup.find('ul', {'class':'f-hide'})
            tags = music_soup.find_all('a', {'class':'u-tag'})
            taglist = []
            for t in tags:
                tag = t.getText()
                taglist.append(tag)
            tagstr = ' '.join(i for i in taglist)
            for music in musics.find_all('a'):
                music_url = music['href'] 
                music_url = 'http://music.163.com' + str(music_url)
                
                line = [lis['title'], new_url, tagstr, music.text, music_url]
                ws.append(line)
                
                #play_dict['music'].append(music.text)
                #play_dict['url'].append(music_url)
                #play_dict['title'].append(lis['title'])
                #play_dict['tag'].append(t)
                print(music.text, '  ', music_url, '  ')
                count += 1
            print("此歌单共%s首" %count)
        #song_list.append(play_dict)
    #return song_list
               
def main():
    wb = Workbook()
    ws = wb.active
    line = ['Playlist', 'Playlist_URL','Tag', 'MusicName', 'URL']
    ws.append(line)
    headers = {'Referer':'http://music.163.com/',
           'Host':'music.163.com',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    init_url = 'http://music.163.com/discover/playlist/?order=hot&cat=%E5%8D%8E%E8%AF%AD'
    get_data(init_url, headers,ws)
    
    wb.save('C:\\Users\\Think\\desktop\\playlists.xlsx')
    
    
if __name__ == '__main__':
    main()