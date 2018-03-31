#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import scrapy
from WebSpider.items import JobItem
from scrapy import Request
import re


class BossSpider(scrapy.Spider):
    name = 'boss'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    def start_requests(self):
        keys = ['大数据', 'hadoop', 'spark']
        for key in keys:
            url = 'https://www.zhipin.com/c101010100/h_101010100/?query=' + key + '&page=1'
            yield Request(url=url, headers=self.headers)

    def parse(self, response):
        links = response.xpath('//div[@class="info-primary"]/h3[@class="name"]/a/@href').extract()
        for link in links:
            true_link = 'https://www.zhipin.com' + link
            print(true_link)
            yield Request(true_link, callback=self.parse_job, headers=self.headers)

        next_url = response.xpath('//a[@class="next"]/@href').extract()
        if next_url:
            url = 'https://www.zhipin.com' + next_url[0]
            yield Request(url)

    def parse_job(self, response):
        try:
            item = JobItem()

            item['job_name'] = response.xpath('//div[@class="name"]/h1/text()').extract()[0]
            # 某一列数据，包含三个
            l = response.xpath('//*[@id="main"]/div[1]/div/div/div[2]/p/text()').extract()
            item['job_exp'] = re.split(r'：+', l[1])[1]
            item['company_name'] = response.xpath('//h3[@class="name"]/a/text()').extract()[0]
            item['company_welfare'] = None
            item['job_pay'] = response.xpath('//span[@class="badge"]/text()').extract()[0]

            item['job_workplace'] = re.split(r'：+', l[0])[1]
            item['job_min_edu'] = re.split(r'：+', l[2])[1]
            # 工作描述
            temps_desc = response.xpath('//div[@class="text"]')[0].xpath('./text()').extract()
            temp_desc = ''
            for i in temps_desc:
                temp_desc += i
            item['job_dec'] = temp_desc
            item['company_size'] = response.xpath('//*[@id="main"]/div[1]/div/div/div[3]/p[1]/text()[2]').extract()[0]
            item['company_ind'] = response.xpath('//a[@ka="job-detail-brandindustry"]/text()').extract()[0]
            yield item
        except IndexError:
            print('index error in ' + response.url)
