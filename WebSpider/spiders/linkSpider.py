#!/usr/bin/env python3
# -*- coding: utf-8 -*

from scrapy.spider import Spider
from WebSpider.items import JobItem
from scrapy import Request

from WebSpider.spiders.ZLZPSpider import JobSpider


def parse_job(response):
    item = JobItem()
    item['job_name'] = response.xpath(
        '//div[@class="inner-left fl"]/h1/text()'
    ).extract()[0]

    test = response.xpath(
        '//p[@class="company-name-t"]/a/text()'
    ).extract()[0]
    for t in test:
        t.encode('utf-8')
    item['company_name'] = test

    item['company_welfare'] = response.xpath(
        '//div[@class="welfare-tab-box"]/span/text()'
    ).extract()
    item['job_pay'] = response.xpath(
        '//ul[@class="terminal-ul clearfix"]/li[1]/strong/text()'
    ).re('(\d+-*\d+元)')[0]
    item['job_workplace'] = response.xpath(
        '//ul[@class="terminal-ul clearfix"]/li[2]/strong/a/text()'
    ).extract()[0]
    item['job_min_edu'] = response.xpath(
        '//ul[@class="terminal-ul clearfix"]/li[6]/strong/text()'
    ).extract()[0]
    desc = response.xpath('//div[@class="tab-inner-cont"]//p/text()').extract()
    item['job_dec'] = desc
    item['company_type'] = response.xpath(
        '//ul[@class="terminal-ul clearfix terminal-company mt20"]/li[2]/strong/text()'
    ).extract()[0]
    # todo: 公司介绍没法完全匹配
    item['company_intro'] = response.xpath(
        '//div[@class="tab-inner-cont"][2]/p/span/span/text()'
    ).extract()
    item['company_size'] = response.xpath(
        '//ul[@class="terminal-ul clearfix terminal-company mt20"]/li[1]/strong/text()'
    ).extract()[0]
    yield item


class linkSpider(Spider):
    name = "link"
    start_urls = ['https://sou.zhaopin.com/jobs/searchresult.ash'
                  'x?jl=全国&kw=大数据&sm=0&p=3&isfilter=0&fl=489&'
                  'isadv=0&sb=1']



