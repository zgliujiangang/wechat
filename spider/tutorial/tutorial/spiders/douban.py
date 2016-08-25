# -*- coding: utf-8 -*-
import scrapy


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["http://douban.com"]
    start_urls = (
        'http://www.http://douban.com/',
    )

    def parse(self, response):
        pass
