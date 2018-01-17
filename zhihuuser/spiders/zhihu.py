# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Spider,Request
from zhihuuser.items import UserItem

class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    user_url = 'http://www.zhihu.com/api/v4/members/{user}?include={include}'
    follows_url = 'http://www.zhihu.com/api/v4/members/{user}/followees?inclide={include}&offset={offset}&limit={limit}'
    followers_url = 'http://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    start_user = 'excited-vczh'
    user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,'\
    'following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,'\
    'following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,'\
    'commercial_question_count,favorite_count,favorited_count,logs_count,included_answers_count,included_articles_count,'\
    'included_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,'\
    'is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,'\
    'is_org_createpin_white_user,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,'\
    'thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,'\
    'org_name,org_homepage,badge[?(type=best_answerer)].topics'
    follow_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    follower_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield Request(self.user_url.format(user=self.start_user,include=self.user_query), self.parse_user)
        yield Request(self.follows_url.format(user=self.start_user,include=self.follow_query,limit=20, offset=0), self.parse_follow)
        yield Request(self.followers_url.format(user=self.start_user,include=self.follower_query, limit=20, offset=0), self.parse_follower)


    def parse_user(self, response):
        result = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item
        print(item['name'])

        yield Request(self.follows_url.format(user=result.get('url_token'),include=self.follow_query,limit=20, offset=0),self.parse_follow)
        yield Request(self.followers_url.format(user=result.get('url_token'),include=self.follower_query,limit=20, offset=0), self.parse_follower)


    def parse_follow(self, response):
        result = json.loads(response.text)

        if 'data' in result.keys():
            for data in result.get('data'):
                yield Request(self.user_url.format(user=data.get('url_token'),include=self.user_query), self.parse_user)

        if 'paging' in result.keys() and result.get('paging').get('is_end') == False:
            next_url = result.get('paging').get('next')
            yield Request(next_url, self.parse_follow)


    def parse_follower(self, response):
        result = json.loads(response.text)
        if 'data' in result.keys():
            for data in result.get('data'):
                yield Request(self.user_url.format(user=data.get('url_token'),include=self.user_query), self.parse_user)

        if 'paging' in result.keys() and result.get('paging').get('is_end') == False:
            next_url = result.get('paging').get('next')
            yield Request(next_url, self.parse_followers)