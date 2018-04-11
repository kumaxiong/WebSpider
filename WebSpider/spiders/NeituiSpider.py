#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy import Request

from WebSpider.items import JobItem
import WebSpider.pipelines as pl

class NeituiSpider(Spider):
    name = 'neitui'

    def start_requests(self):
        keys = ['大数据', 'hadoop', 'spark']
        for key in keys:
            url = 'http://www.neitui.me/?name=job&handle=lists&city=城市&keyword=' + key
            yield Request(url=url)

    # start_urls = ['http://www.neitui.me/?name=job&handle=lists&city=城市&keyword=大数据']

    def parse(self, response):

        cards = response.xpath('//div[@class="media"]')
        for card in cards:
            item = JobItem()
            for field in item.fields:
                item[field] = None
            item['job_issue'] = 'neitui'
            item['job_name'] = card.xpath('.//div[@class="mt5 clearfix"]/a/text()').extract()[0]
            item['company_name'] = card.xpath('.//a[@class="blue-gray"]/text()').extract()[0]
            item['job_pay'] = card.xpath('.//span[@class="orange mr10"]/text()').extract()[0]
            url = card.xpath('.//div[@class="mt5 clearfix"]/a/@href').extract()[0]
            true_link = 'http://www.neitui.me' + url
            item['job_url'] = true_link
            yield Request(true_link, callback=self.parse_job, meta={'item': item})

        next_url = response.xpath('//a[@aria-label="Next"]/@href').extract()
        if next_url:
            next_url = 'http://www.neitui.me/' + next_url[0]
            yield Request(next_url)

    def parse_job(self, response):
        print('parse_job')
        item = response.meta['item']
        item['company_ind'] = response.xpath('//div[@class="row"]')[3].xpath('.//span[@class="grey"]/text()').extract()[
            0]
        item['company_size'] = \
            response.xpath('//div[@class="row"]')[3].xpath('.//span[@class="grey"]/text()').extract()[2]
        item['job_exp'] = response.xpath('//div[@class="font16 mt10 mb10"]/span/text()').extract()[1]
        try:
            item['job_min_edu'] = response.xpath('//span[@data-default="学历不限"]/text()').extract()[0]
        except IndexError:
            item['job_min_edu'] = '学历不限'
        item['job_workplace'] = response.xpath('//div[@class="font16 mt10 mb10"]/span/text()').extract()[-2]
        l = response.xpath('//div[@class="font16 mt10 mb10"]/span/text()').extract()
        if len(l) == 4:
            item['job_workplace'] = response.xpath('//div[@class="font16 mt10 mb10"]/span/text()').extract()[-1]

        desc_temps = response.xpath('//div[@class="mb20 jobdetailcon"]/text()').extract()
        desc = ''
        for i in desc_temps:
            desc = desc + i

        item['job_dec'] = desc
        print(item['job_name'])
        yield item
