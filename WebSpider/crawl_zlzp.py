#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from scrapy import cmdline

name = 'zlzp'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())