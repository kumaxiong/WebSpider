#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scrapy


class NovelSpider(scrapy.Spider):
    name = "zlzp"
    allowed_domains = ["zhaopin.com"]
    start_urls = [
        "https://sou.zhaopin.com/jobs/searchresult.ashx?jl=全国&kw=大数据&sm=0&p=3&isfilter=0&fl=489&isadv=0&sb=1"
    ]

    def parse(self, response):
        for doc in response.xpath('//td[@class="zwmc"]'):
            link = doc.xpath('div/a/@href').extract()
            print('岗位信息对应地址', link)
