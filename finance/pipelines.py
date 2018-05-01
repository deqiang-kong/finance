# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import cursors

from finance.items import ColumnItem, ColumnDetailItem
from finance.util.connect import connect_net
from twisted.enterprise import adbapi

class FinancePipeline(object):
    # ******************
    # 爬虫启动
    def open_spider(self, spider):
        print(spider.name + " 爬虫启动.............")
        self.conn = connect_net()

        # # 创建数据表
        # create_column_list_table(self.conn)
        # print(spider.name + " 爬虫启动........2222.....")
        # create_column_detail_table(self.conn)
        # print(spider.name + " 爬虫启动.......3333......")
        # self.dailys = get_column_list(self.conn)
        # self.dailys_detail = get_dailys_detail(self.conn)
        # print(spider.name + " 爬虫启动111111.............")

    ##
    ##
    # 爬虫执行
    def process_item(self, item, spider):
        # # 专栏数据入库
        if isinstance(item, ColumnItem):
            print(spider.name + " 专栏数据入库............." + item['title'])
        #     store_column(item, self.conn, self.dailys)
        #
        elif isinstance(item, ColumnDetailItem):
            print(spider.name + " 专栏详情入库.............")
        #     store_detail(item, self.conn, self.dailys_detail)

        return item

    # 爬虫结束
    def close_spider(self, spider):
        print(spider.name + " 爬虫结束.............")
        self.conn.close()

