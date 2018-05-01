# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

from finance.items import ColumnItem, ColumnDetailItem
from finance.util.connect import connect_net, create_table, dbparams
from twisted.enterprise import adbapi


class FinancePipeline(object):
    # ******************
    # 爬虫启动
    def open_spider(self, spider):
        print(spider.name + " 爬虫启动.............")
        self.conn = connect_net()
        create_table()

        # 数据库连接池
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql_list = None
        self._sql_detail = None

    # 爬虫结束
    def close_spider(self, spider):
        print(spider.name + " 爬虫结束.............")
        self.conn.close()

    ##
    # 爬虫执行
    def process_item(self, item, spider):
        # # 专栏数据入库
        if isinstance(item, ColumnItem):
            print(spider.name + " 专栏数据入库............." + item['title'])
            flag = self.get_column_list(self.conn, item)
            if flag:
                # 异步插入
                defer = self.dbpool.runInteraction(self.insert_list_item, item)
                defer.addErrback(self.handle_error, item, spider)

        elif isinstance(item, ColumnDetailItem):
            print(spider.name + " 专栏详情入库.............")
            flag = self.get_column_detail(self.conn, item)
            if flag:
                # 异步插入
                defer = self.dbpool.runInteraction(self.insert_detail_item, item)
                defer.addErrback(self.handle_error, item, spider)

        return item

    # 判断数据是否已存在
    def get_column_list(self, conn, item):
        cur = conn.cursor()
        query = "select title from column_list where column_id = '" + item['id'] + "'"
        flag = cur.execute(query)
        if flag == 0:
            return True
        else:
            return False

    # 判断数据是否已存在
    def get_column_detail(self, conn, item):
        cur = conn.cursor()
        query = "select title from column_detail where column_id = '" + item['id'] + "'"
        flag = cur.execute(query)
        if flag == 0:
            return True
        else:
            return False

    # 将方法变成属性
    @property
    def sql_list(self):
        if not self._sql_list:
            self._sql_list = """
                   insert into column_list(column_id,title,img_url,introduce,author,author_portrait,pageview,issue_time,store_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                   """
            return self._sql_list
        return self._sql_list

    def insert_list_item(self, cursor, item):
        cursor.execute(self.sql_list, (
            item['id'], item['title'], item['img_url'], item['introduce'], item['author'], item['author_portrait'],
            item['pageview'],
            item['issue_time'], datetime.datetime.now()))

    @property
    def sql_detail(self):
        if not self._sql_detail:
            self._sql_detail = """
                      insert into column_detail(column_id,title,content,issue_time,store_time) values(%s,%s,%s,%s,%s)
                      """
            return self._sql_detail
        return self._sql_detail

    #
    def insert_detail_item(self, cursor, item):
        cursor.execute(self.sql_detail, (
            item['id'], item['title'], item['content'],
            item['issue_time'], datetime.datetime.now()))

    # 错误输出
    def handle_error(self, error, item, spider):
        print('=' * 10 + "error" + '=' * 10)
        print(error)
        print('=' * 10 + "error" + '=' * 10)
