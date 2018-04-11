#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from scrapy import Request
from scrapy.spiders import Spider
from WebSpider.items import JobItem


class Job51Spider(Spider):
    name = 'job51'
    allowed_domains = ["search.51job.com", "jobs.51job.com"]

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
    }

    def start_requests(self):
        url = 'http://search.51job.com/list/000000,000000,0000,00,9,99,%25E5%25A4%25A7%25E6%2595%25B0%25E6%258D%25AE,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        yield Request(url=url, headers=self.headers)

    def parse(self, response):
        jobs = response.xpath("//div[@class='el']/p/span/a/@href").extract()
        for job in jobs:

            # 初始化item
            item = JobItem()
            for field in item.fields:
                item[field] = None

            item['job_issue'] = 'job51'
            item['job_url'] = str(job)

            # 过滤公司总页
            flag = re.findall('https://jobs.51job.com/all/',job)
            if flag:
                continue
            yield Request(job, callback=self.parse_job, headers=self.headers, meta={'item': item})

        # 翻页
        next_url = response.xpath('//li[@class="bk"][2]/a/@href').extract()
        if next_url:
            print(next_url)
            yield Request(next_url[0], headers=self.headers)

    def parse_job(self, response):
        item = response.meta['item']
        item['job_name'] = response.xpath('//div[@class="cn"]/h1/text()').extract()[0]
        item['job_exp'] = response.xpath('//div[@class="t1"]/span[1]/text()').extract()[0]
        item['company_name'] = response.xpath('//p[@class="cname"]/a/text()').extract()[0]

        welfares = response.xpath('//p[@class="t2"]/span/text()').extract()
        company_welfare = ''
        for i in welfares:
            company_welfare = company_welfare + i + ','
        item['company_welfare'] = company_welfare
        item['job_pay'] = response.xpath('//div[@class="cn"]/strong/text()').extract()[0]
        item['job_workplace'] = response.xpath('//span[@class="lname"]/text()').extract()[0]
        item['job_min_edu'] = response.xpath('//div[@class="t1"]/span/text()').extract()[1]
        decs = response.xpath('//div[@class="bmsg job_msg inbox"]/text()').extract()
        dec = ''
        for i in decs:
            dec = dec + i

        item['job_dec'] = dec
        l = response.xpath('//p[@class="msg ltype"]/text()').extract()[0]
        result = re.sub(r'[\t|\r|\n|\xa0]', '', l)
        result = re.split('      ', result)
        item['company_size'] = result[1].strip()
        item['company_ind'] = result[3].strip()
        yield item
