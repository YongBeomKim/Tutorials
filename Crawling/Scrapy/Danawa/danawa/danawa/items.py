# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DanawaCpuItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    reg_date = scrapy.Field()
    crawled_date = scrapy.Field()