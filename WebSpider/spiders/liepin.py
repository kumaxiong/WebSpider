# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Request

from WebSpider.items import JobItem


class LiepinSpider(scrapy.Spider):
    name = "liepin"
    allowed_domains = ["www.liepin.com"]
    start_urls = [
        'https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&d_sfrom=search_fp&key=大数据']

    # def start_requests(self):
    #

    def parse(self, response):
        cards = response.xpath('//div[@class="sojob-item-main clearfix"]')
        for card in cards:
            item = JobItem()
            # 初始化item
            for field in item.fields:
                item[field] = None
            link = card.xpath('.//h3/a/@href').extract()[0]
            item['job_url'] = link
            item['job_issue'] = 'liepin'
            item['company_ind'] = card.xpath('.//a[@class="industry-link"]/text()').extract()[0]
            yield Request(link, meta={'item': item}, callback=self.parse_job)

    def parse_job(self, response):
        item = response.meta['item']
        item['job_name'] = response.xpath('//div[@class="title-info"]/h1/text()').extract()[0]
        job_pay = response.xpath('//p[@class="job-item-title"]/text()').extract()[0]
        job_pay = re.findall('(\d+-\d+万).*', job_pay)
        if len(job_pay) == 0:
            job_pay = '面议'
            item['job_pay'] = job_pay
        else:
            item['job_pay'] = job_pay[0]

        job_qua = response.xpath('//div[@class="job-qualifications"]/span/text()').extract()

        item['job_min_edu'] = job_qua[0]
        item['job_exp'] = job_qua[1]

        welfares = response.xpath('//div[@class="tag-list"]/span/text()').extract()
        wel = ''
        for i in welfares:
            wel = wel + i + ','

        item['company_welfare'] = wel
        item['company_name'] = response.xpath('//div[@class="title-info"]/h3/a/text()').extract()[0]
        desc = ''
        temp_descs = response.xpath('//div[@class="job-item main-message job-description"]/div/text()').extract()
        for i in temp_descs:
            desc = desc + i

        item['job_dec'] = desc

        item['job_workplace'] = response.xpath('//p[@class="basic-infor"]/span/a/text()').extract()[0]
        yield item
