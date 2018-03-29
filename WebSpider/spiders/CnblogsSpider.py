#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider, Rule
from scrapy.linkextractors import LinkExtractor
from WebSpider.items import CnblogItem
from scrapy import Request


def parse_detail(response):
    """处理新闻详情页数据回调方法"""
    # print(response.url)
    title = response.xpath('//div[@id="news_title"]/a/text()')[0].extract()
    postor = response.xpath('//span[@class="news_poster"]/a/text()')[0].extract()
    pubtime = response.xpath('//span[@class="time"]/text()')[0].extract()
    content = response.xpath('//div[@id="news_body"]/p/text()').extract()

    item = CnblogItem()
    item['title'] = title
    item['postor'] = postor
    item['pubtime'] = pubtime
    item['content'] = content

    yield item


class CnblogsSpider(Spider):
    name = 'cnblog'
    start_urls = [
        'https://news.cnblogs.com/n/page/1/'
    ]

    headers = {
        'x-devtools-emulate-network-conditions-client-id': "5f2fc4da-c727-43c0-aad4-37fce8e3ff39",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'dnt': "1",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.8,en;q=0.6",
        'cookie': "__c=1501326829; lastCity=101020100; __g=-; __l=r=https%3A%2F%2Fwww.google.com.hk%2F&l=%2F; __a=38940428.1501326829..1501326829.20.1.20.20; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1501326839; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1502948718; __c=1501326829; lastCity=101020100; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1501326839; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1502954829; __l=r=https%3A%2F%2Fwww.google.com.hk%2F&l=%2F; __a=38940428.1501326829..1501326829.21.1.21.21",
        'cache-control': "no-cache",
        'postman-token': "76554687-c4df-0c17-7cc0-5bf3845c9831"
    }

    def parse(self, response):
        next_text = response.xpath('//div[@class="pager"]/a/text()')[-1].extract()
        if next_text == 'Next >':
            offset = response.xpath('//div[@class="pager"]/a/@href')[-1].extract()
            next_url = 'https://news.cnblogs.com' + offset
            Request(url=next_url, headers=self.headers)

        articles = response.xpath('//div[@class="news_block"]/div[@class="content"]/h2/a/@href').extract()
        for article in articles:
            article_url = 'https: // news.cnblogs.com' + article
            Request(article_url, headers=self.headers, callback=parse_detail)
