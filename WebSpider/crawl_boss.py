#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from scrapy import cmdline

name = 'boss'
cmd = 'scrapy crawl {0} --logfile=boss.log'.format(name)
cmdline.execute(cmd.split())
