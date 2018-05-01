# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy



# 专栏列表数据字段
class ColumnItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    detail_url = scrapy.Field()
    introduce = scrapy.Field()
    author = scrapy.Field()
    author_portrait = scrapy.Field()
    issue_time = scrapy.Field()
    pageview = scrapy.Field()

    pass


# 专栏详情数据字段
class ColumnDetailItem(scrapy.Item):
    detail_url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

    author = scrapy.Field()
    browse = scrapy.Field()
    source = scrapy.Field()
    compile = scrapy.Field()
    issue_time = scrapy.Field()

    pass
