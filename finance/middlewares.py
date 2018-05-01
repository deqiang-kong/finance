# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#
import time

from scrapy import signals
from selenium import webdriver
from scrapy.http.response.html import HtmlResponse


# Selenium 动态网页爬去中间件
class SeleniumDownloadMiddleware(object):
    def __init__(self):
        # chromedriver文件路径
        driver_path = r"/Users/kaipai/Desktop/Tools/chromedriver"
        self.driver = webdriver.Chrome(executable_path=driver_path)

    def process_request(self, request, spider):
        self.driver.get(request.url)
        # time.sleep(1)
        try:
            index = 0
            while True:
                # showMore = self.driver.find_element_by_class_name('article-loading')
                index = index + 1
                showMore = self.driver.find_element_by_id('custom-click-loade')
                showMore.click()

                if index > 2:
                    break
                time.sleep(4)
                if not showMore:
                    break
        except:
            pass
        source = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=source, request=request, encoding='utf-8')
        return response
