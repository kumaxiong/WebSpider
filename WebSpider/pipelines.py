# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class JobPipeline(object):
    quotes_name = 'quotes'
    author_name = 'author'

    def __init__(self, settings):
        self.settings = settings

    def process_item(self, item, spider):
        print(item)
        if spider.name == "zlzp":
            sql = "insert into job (job_name,job_pay,job_workplace,job_dec,job_min_edu,job_exp,company_welfare,company_name,company_ind,company_size) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # 执行sql语句
            self.cursor.execute(sql, (item['job_name'], item['job_pay'],item['job_workplace'], item['job_dec'],
                                      item['job_min_edu'],item['job_exp'],item['company_welfare'],item['company_name'],
                                      item['company_ind'],item['company_size'],))
        elif spider.name == "author":
            pass
            # sqltext = self.authorInsert.format(
            #     name=pymysql.escape_string(item['name']),
            #     birthdate=pymysql.escape_string(item['birthdate']),
            #     bio=pymysql.escape_string(item['bio']))
            # self.cursor.execute(sqltext)
        else:
            spider.log('Undefined name: %s' % spider.name)

        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        # 连接数据库
        self.connect = pymysql.connect(
            host=self.settings.get('MYSQL_HOST'),
            port=self.settings.get('MYSQL_PORT'),
            db=self.settings.get('MYSQL_DBNAME'),
            user=self.settings.get('MYSQL_USER'),
            passwd=self.settings.get('MYSQL_PASSWD'),
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
        self.connect.autocommit(True)

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
