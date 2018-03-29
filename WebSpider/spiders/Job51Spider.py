#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import Spider
from WebSpider.items import JobItem


class Job51Spider(Spider):
    name = 'job51'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
    }

    def start_requests(self):
        url = 'http://search.51job.com/list/000000,000000,0000,00,9,99,%25E5%25A4%25A7%25E6%2595%25B0%25E6%258D%25AE,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        yield Request(url=url, headers=self.headers)

    def parse(self, response):
        jobs = response.xpath("//div[@class='el']/p/span/a/@href").extract()
        for job in jobs:
            yield Request(job, callback=self.parse_job, headers=self.headers)
        next_url = response.xpath('//li[@class="bk"][2]/a/@href').extract()
        if next_url:
            yield Request(next_url[0], headers=self.headers)

    def parse_job(self, response):
        item = JobItem()
        item['job_name'] = response.xpath('//div[@class="cn"]/h1/text()').extract()[0]
        item['job_exp'] = response.xpath('//div[@class="t1"]/span[1]/text()').extract()[0]
        item['company_name'] = response.xpath('//p[@class="cname"]/a/@href').extract()[0]
        item['company_welfare'] = response.xpath('//p[@class="t2"]/span/text()').extract()
        item['job_pay'] = response.xpath('//div[@class="cn"]/strong/text()').extract()[0]
        item['job_workplace'] = response.xpath('//span[@class="lname"]/text()').extract()[0]
        item['job_min_edu'] = None
        item['job_dec'] = response.xpath('//div[@class="bmsg job_msg inbox"]/p/text()').extract()
        item['company_size'] = None
        item['company_ind'] = None
        yield item
