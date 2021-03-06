# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy_redis.spiders import RedisSpider
from weiboMaster.items import WeibomasterItem
from redis import Redis


class WeiboSpider(RedisSpider):
    name = "weibo"
    redis_key = 'weibo_urls'
    # allowed_domains = ["http://m.weibo.cn"]

    def parse(self, response):
        if response.status is 200:
            self.logger.info('Parse function called on %s', response.url)
            item = WeibomasterItem()
            rep = json.loads(response.body_as_unicode())
            print(response.url + '  crawl done!')
            for data in rep['data']:
                item['comment_id'] = data['id']
                item['name'] = data['user']['screen_name']
                item['text'] = data['text']
                item['source'] = data['source']
                if 'reply_text' in data:
                    item['reply_text'] = data['reply_text']
                else:
                    item['reply_text'] = '-'
                s = data['text']
                if (s.find('@') != -1) & (s.find('</') != -1):
                    item['reply_name'] = s[s.find('@')+1:s.find('</')]
                else:
                    item['reply_name'] = '-'
                yield item
        else:
            print('response error')
