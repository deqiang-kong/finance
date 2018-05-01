# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymysql import cursors

from finance import items
from finance.items import ColumnItem
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
        # elif item_name is items.column_detail:
        #     print(spider.name + " 专栏详情入库............." + item_name)
        #     store_detail(item, self.conn, self.dailys_detail)

        return item

    # 爬虫结束
    def close_spider(self, spider):
        print(spider.name + " 爬虫结束.............")
        self.conn.close()


class JianshuTwistedPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'jianshu2',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        # 数据库连接池
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                insert into article(id,title,content,author,avatar,pub_time,origin_url,article_id) values(null,%s,%s,%s,%s,%s,%s,%s)
                """
            return self._sql
        return self._sql


    def process_item(self, item, spider):
        # 异步插入
        defer = self.dbpool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handle_error, item, spider)

    #
    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (
            item['title'], item['content'], item['author'], item['avatar'], item['pub_time'], item['origin_url'],
            item['article_id']))

    # 错误输出
    def handle_error(self, error, item, spider):
        print('=' * 10 + "error" + '=' * 10)
        print(error)
        print('=' * 10 + "error" + '=' * 10)
