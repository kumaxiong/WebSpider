#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from scrapy import cmdline

name = 'neitui'
cmd = 'scrapy crawl {0} --logfile=neitui.log'.format(name)
cmdline.execute(cmd.split())
