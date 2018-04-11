# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

import pymysql
from scrapy.exceptions import DropItem


class JobPipeline(object):
    quotes_name = 'quotes'
    author_name = 'author'

    def __init__(self, settings):
        self.settings = settings

    def process_item(self, item, spider):
        # print(item)
        query_sql = "SELECT company_name,job_issue FROM job WHERE company_name LIKE %s"
        self.cursor.execute(query_sql, ('%' + item['company_name'] + '%'))
        result = self.cursor.fetchall()
        result2 = self.cursor.execute('SELECT * FROM job WHERE job_url = %s', (item['job_url']))
        if result2:
            raise DropItem('you have crawled one in ',item['job_url'])
        elif result and result[0][1] != str(spider.name):
            raise DropItem('company has crawled in ', result[0]['job_issue'], 'but now ' + spider.name)
        else:
            sql = "insert into job (job_name,job_pay,job_workplace,job_dec,job_min_edu,job_exp,company_welfare,company_name,company_ind,company_size,job_url,job_issue) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # 执行sql语句
            self.cursor.execute(sql, (item['job_name'], item['job_pay'], item['job_workplace'], item['job_dec'],
                                      item['job_min_edu'], item['job_exp'], item['company_welfare'],
                                      item['company_name'],
                                      item['company_ind'], item['company_size'],
                                      item['job_url'], item['job_issue']))
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


class JobPrePipeline(object):
    quotes_name = 'quotes'
    author_name = 'author'

    def __init__(self, settings):
        self.settings = settings

    def process_item(self, item, spider):

        print(item)
        # 计算学历
        item['job_min_edu'] = get_edu(item['job_min_edu'])
        # 计算工作地点
        item['job_workplace'] = get_zone(item['job_workplace'])

        if spider.name == "zlzp":
            pay = item['job_pay']
            result = re.findall('(\d+)-(\d+)元', pay)
            if result:
                r = (int(result[0][0]) + int(result[0][1])) / 2
                item['job_pay'] = int(r)
            elif re.findall('(\d+)元', pay):
                result = re.findall('(\d+)元', pay)
                item['job_pay'] = int(result[0])

            exp = item['job_exp']
            result = re.findall('(\d+)-(\d+)年', exp)
            if result:
                item['job_exp'] = (int(result[0][0]) + int(result[0][1])) / 2
            elif exp == '不限' or exp == '无经验':
                item['job_exp'] = 0
            elif re.findall('(\d+)年.*', exp):
                result = re.findall('(\d+)年.*', exp)
                item['job_exp'] = int(result[0][0])

        if spider.name == 'neitui':
            # 计算工资，工资形式 0k-123k
            pay = item['job_pay']
            result = re.findall('(\d+)k-(\d+)k', pay)
            a = (int(result[0][0]) + int(result[0][1])) * (1000 / 2)
            item['job_pay'] = int(a)
            # 计算工作
            s = item['job_exp']
            result = re.findall('(\d+)-(\d+)年', s)
            if result:
                a = (int(result[0][0]) + int(result[0][1])) / 2
                item['job_exp'] = int(a)
            elif re.findall('-(\d+)年', s):
                result = re.findall('-(\d+)年', s)
                a = int(result[0][0])
                item['job_exp'] = a
        if spider.name == 'liepin':
            # 计算工资，工资形式 23-42万、面议
            pay = item['job_pay']
            result = re.findall('(\d+)k-(\d+)万', pay)
            if result:
                a = (int(result[0][0]) + int(result[0][1])) * (10000 / 24)
            else:
                a = 0
            item['job_pay'] = int(a)
            # 计算工作
            s = item['job_exp']
            result = re.findall('(\d+)年.*?', s)
            if result:
                a = int(result[0])
                item['job_exp'] = a
            else:
                item['job_exp'] = 0
        if spider.name == 'job51':
            # 计算工资
            pay = item['job_pay']
            result = re.findall('(\d+\.?\d*)-(\d+)万/年', pay)
            if result:
                r = (float(result[0][0]) + float(result[0][1])) / 12 * 10000
                r = r / 2
                item['job_pay'] = int(r)
            elif re.findall('(\d+\.?\d*)-(\d+\.?\d*)万/月', pay):
                result = re.findall('(\d+\.?\d*)-(\d+\.?\d*)万/月', pay)
                r = (float(result[0][0]) + float(result[0][1])) * 10000
                r = r / 2
                item['job_pay'] = int(r)
            elif re.findall('(\d+\.?\d*)-(\d+\.?\d*)千/月', pay):
                result = re.findall('(\d+\.?\d*)-(\d+\.?\d*)千/月', pay)
                r = (float(result[0][0]) + float(result[0][1]))
                r = r / 2
                item['job_pay'] = int(r)
            elif re.findall('(\d+)元/天', pay):
                result = re.findall('(\d+)元/天', pay)
                r = float(result[0]) * 20
                item['job_pay'] = int(r)

            # 计算工作经验
            exp = item['job_exp']
            result = re.findall('(\d+)年工作经验', exp)
            if result:
                f = float(result[0])
                item['job_exp'] = int(f)
            elif re.findall('(\d+)-(\d+)年经验', exp):
                result = re.findall('(\d+)-(\d+)年经验', exp)
                f = int(result[0][0]) + int(result[0][1])
                f = f / 2
                item['job_exp'] = int(f)
            elif re.findall('(\d+)年以上经验', exp):
                result = re.findall('(\d+)年以上经验', exp)
                f = float(result[0])
                item['job_exp'] = int(f)
            else:
                item['job_exp'] = 0
            # 计算最低学历
        if spider.name == 'boss':
            pay = item['job_pay']
            result = re.findall('(\d+)K-(\d+)K', pay)
            if result:
                r = int(result[0][1]) + int(result[0][0])
                r = r / 2
                item['job_pay'] = int(r)
            else:
                item['job_pay'] = 0
            exp = item['job_exp']
            result = re.findall('(\d+)-(\d+)年', exp)
            if result:
                r = int(result[0][0]) + int(result[0][1])
                r = r / 2
                item['job_exp'] = int(r)
            elif re.findall('(\d+)年.*?', exp):
                result = re.findall('(\d+)年.*?', exp)
                r = int(result[0])
                item['job_exp'] = r
            else:
                item['job_exp'] = 0
        sql = "insert into job_pre (job_name,job_pay,job_workplace,job_dec,job_min_edu,job_exp,company_welfare,company_name,company_ind,company_size,job_url, job_issue) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # 执行sql语句
        self.cursor.execute(sql, (item['job_name'], item['job_pay'], item['job_workplace'], item['job_dec'],
                                  item['job_min_edu'], item['job_exp'], item['company_welfare'],
                                  item['company_name'],
                                  item['company_ind'], item['company_size'],
                                  item['job_url'], item['job_issue']))
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


def get_edu(edu):
    if edu == '统招本科':
        edu = '本科'
    if len(edu) > 2:
        edu = edu[0:2]
    edus = ['不限', '中技', '中专', '高中', '大专', '本科', '硕士', '博士', ]
    try:
        a = edus.index(edu)
    except ValueError:
        print(edu)
        a = 0
    return a


def get_zone(zone_name):
    s = '''北京市 010
    上海市 021
    天津市 022
    重庆市 023
    香港 852
    邯郸市 0310
    石家庄 0311
    保定市 0312
    张家口 0313
    承德市 0314
    唐山市 0315
    廊坊市 0316
    沧州市 0317
    衡水市 0318
    邢台市 0319
    秦皇岛 0335
    衢州市 0570
    杭州市 0571
    湖州市 0572
    嘉兴市 0573
    宁波市 0574
    绍兴市 0575
    台州市 0576
    温州市 0577
    丽水市 0578
    金华市 0579
    舟山市 0580
    沈阳市 024
    铁岭市 0410
    大连市 0411
    鞍山市 0412
    抚顺市 0413
    本溪市 0414
    丹东市 0415
    锦州市 0416
    营口市 0417
    阜新市 0418
    辽阳市 0419
    朝阳市 0421
    盘锦市 0427
    葫芦岛 0429
    武汉市 027
    襄城市 0710
    鄂州市 0711
    孝感市 0712
    黄州市 0713
    黄石市 0714
    咸宁市 0715
    荆沙市 0716
    宜昌市 0717
    恩施市 0718
    十堰市 0719
    随枣市 0722
    荆门市 0724
    江汉市 0728
    南京市 025
    无锡市 0510
    镇江市 0511
    苏州市 0512
    南通市 0513
    扬州市 0514
    盐城市 0515
    徐州市 0516
    淮阴市 0517
    淮安市 0517
    连云港 0518
    常州市 0519
    泰州市 0523
    新余市 0790
    南昌市 0791
    九江市 0792
    上饶市 0793
    临川市 0794
    宜春市 0795
    吉安市 0796
    赣州市 0797
    景德镇 0798
    萍乡市 0799
    鹰潭市 0701
    忻州市 0350
    太原市 0351
    大同市 0352
    阳泉市 0353
    榆次市 0354
    长治市 0355
    晋城市 0356
    临汾市 0357
    离石市 0358
    运城市 0359
    临夏市 0930
    兰州市 0931
    定西市 0932
    平凉市 0933
    西峰市 0934
    武威市 0935
    张掖市 0936
    酒泉市 0937
    天水市 0938
    甘南州 0941
    白银市 0943
    菏泽市 0530
    济南市 0531
    青岛市 0532
    淄博市 0533
    德州市 0534
    烟台市 0535
    淮坊市 0536
    济宁市 0537
    泰安市 0538
    临沂市 0539
    阿城市 0450
    哈尔滨 0451
    齐齐哈尔 0452
    牡丹江 0453
    佳木斯 0454
    绥化市 0455
    黑河市 0456
    加格达奇 0457
    伊春市 0458
    大庆市 0459
    广州市 020
    韶关市 0751
    惠州市 0752
    梅州市 0753
    汕头市 0754
    深圳市 0755
    珠海市 0756
    佛山市 0757
    肇庆市 0758
    湛江市 0759
    中山市 0760
    河源市 0762
    清远市 0763
    顺德市 0765
    云浮市 0766
    潮州市 0768
    东莞市 0769
    汕尾市 0660
    潮阳市 0661
    阳江市 0662
    揭西市 0663
    成都市 028
    涪陵市 0810
    重庆市 0811
    攀枝花 0812
    自贡市 0813
    永川市 0814
    绵阳市 0816
    南充市 0817
    达县市 0818
    万县市 0819
    遂宁市 0825
    广安市 0826
    巴中市 0827
    泸州市 0830
    宜宾市 0831
    内江市 0832
    乐山市 0833
    西昌市 0834
    雅安市 0835
    康定市 0836
    马尔康 0837
    德阳市 0838
    广元市 0839
    泸州市 0840
    岳阳市 0730
    长沙市 0731
    湘潭市 0732
    株州市 0733
    衡阳市 0734
    郴州市 0735
    常德市 0736
    益阳市 0737
    娄底市 0738
    邵阳市 0739
    吉首市 0743
    张家界 0744
    怀化市 0745
    永州冷 0746
    商丘市 0370
    郑州市 0371
    安阳市 0372
    新乡市 0373
    许昌市 0374
    平顶山 0375
    信阳市 0376
    南阳市 0377
    开封市 0378
    洛阳市 0379
    焦作市 0391
    鹤壁市 0392
    濮阳市 0393
    周口市 0394
    漯河市 0395
    驻马店 0396
    三门峡 0398
    昭通市 0870
    昆明市 0871
    大理市 0872
    个旧市 0873
    曲靖市 0874
    保山市 0875
    文山市 0876
    玉溪市 0877
    楚雄市 0878
    思茅市 0879
    景洪市 0691
    潞西市 0692
    东川市 0881
    临沧市 0883
    六库市 0886
    中甸市 0887
    丽江市 0888
    银川市 0951
    石嘴山 0952
    吴忠市 0953
    固原市 0954
    儋州市 0890
    海口市 0898
    三亚市 0899
    拉萨市 0891
    日喀则 0892
    山南市 0893
    长春市 0431
    吉林市 0432
    延吉市 0433
    四平市 0434
    通化市 0435
    白城市 0436
    辽源市 0437
    松原市 0438
    浑江市 0439
    珲春市 0440
    防城港 0770
    南宁市 0771
    柳州市 0772
    桂林市 0773
    梧州市 0774
    玉林市 0775
    百色市 0776
    钦州市 0777
    河池市 0778
    北海市 0779
    贵阳市 0851
    遵义市 0852
    安顺市 0853
    都均市 0854
    凯里市 0855
    铜仁市 0856
    毕节市 0857
    六盘水 0858
    兴义市 0859
    西安市 029
    咸阳市 0910
    延安市 0911
    榆林市 0912
    渭南市 0913
    商洛市 0914
    安康市 0915
    汉中市 0916
    宝鸡市 0917
    铜川市 0919
    西宁市 0971
    海东市 0972
    同仁市 0973
    共和市 0974
    玛沁市 0975
    玉树市 0976
    德令哈 0977
    澳门 853
    海拉尔 0470
    呼和浩特 0471
    包头市 0472
    乌海市 0473
    集宁市 0474
    通辽市 0475
    赤峰市 0476
    东胜市 0477
    临河市 0478
    锡林浩特 0479
    乌兰浩特 0482
    阿拉善左旗 0483
    福州市 0591
    厦门市 0592
    宁德市 0593
    莆田市 0594
    泉州市 0595
    晋江市 0595
    漳州市 0596
    龙岩市 0597
    三明市 0598
    南平市 0599
    滁州市 0550
    合肥市 0551
    蚌埠市 0552
    芜湖市 0553
    淮南市 0554
    马鞍山 0555
    安庆市 0556
    宿州市 0557
    阜阳市 0558
    黄山市 0559
    淮北市 0561
    铜陵市 0562
    宣城市 0563
    六安市 0564
    巢湖市 0565
    贵池市 0566
    阿莲  886
    安定 887
    安平 888
    八德 889
    八里 890
    白河 891
    白沙 892
    板桥 893
    褒忠 894
    宝山 895
    卑南 896
    北斗 897
    北港 898
    北门 899
    北埔 900
    北投 901
    补子 902
    布袋 903
    草屯 904
    长宾 905
    长治 906
    潮州 907
    车城 908
    城中区 909
    成功 910
    池上 911
    春日 912
    刺桐 913'''
    result = re.findall('' + zone_name + '.*? (\d+)', s)
    if result:
        return int(result[0])
    elif re.findall('' + zone_name[0:2] + '.*? (\d+)', s):
        result = re.findall('' + zone_name[0:2] + '.*? (\d+)', s)
        return int(result[0])
    else:
        return -1
