# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    job_name = scrapy.Field()  # 工作名称
    job_pay = scrapy.Field()  # 工资
    job_workplace = scrapy.Field()  # 工作地点
    job_dec = scrapy.Field()  # 工作描述（技能提取）
    job_min_edu = scrapy.Field()  # 最低学历
    job_exp = scrapy.Field()  # 工作经验
    company_welfare = scrapy.Field()  # 公司福利
    company_name = scrapy.Field()  # 公司名称
    company_ind = scrapy.Field()  # 公司行业
    company_size = scrapy.Field()  # 公司规模
    job_url = scrapy.Field()  # 工作详情页链接
    job_issue = scrapy.Field()  # 工作来源 zlzp、51job等
