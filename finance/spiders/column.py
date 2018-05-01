import scrapy
from scrapy.spiders import CrawlSpider

from finance.util.strutil import getStrFirst
from ..items import ColumnItem, ColumnDetailItem


# 金色财经专栏数据爬取
class FinanceSpider(CrawlSpider):
    # 爬虫名称
    name = "finan"
    # 可选，筛选器，允许域范围
    # allowd_domains = ['jinse.com']
    # 爬取的urls
    start_urls = ['http://www.jinse.com/columns/']

    # rules = (
    #     Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    # )

    # 解析专栏列表
    def parse(self, response):
        print("\n\n " + self.name + " parse---------------start")

        # 解析列表
        img_temp = response.xpath("//div[@class='article-main']/ol")
        # 没有办法获取到数据
        # data_temp = response.xpath("//div[@class='article-main']/ol/ul")
        data_temp = response.xpath("//div[@class='article-main']//ul")

        img_list = []
        data_list = []
        for bean in img_temp:
            id = bean.xpath(".//@data-information-id").get()
            detail_url = bean.xpath(".//a/@href").get().strip()
            img_url = bean.xpath(".//a/img/@src").get().strip()
            img_dict = {}
            img_dict['id'] = id
            img_dict['detail_url'] = detail_url
            img_dict['img_url'] = img_url
            # print(img_dict)
            img_list.append(img_dict)

        for bean in data_temp:
            title = bean.xpath(".//a/@title").get().strip()
            detail_url = bean.xpath(".//a/@href").get().strip()
            # 简介
            introduce = bean.xpath(".//li/text()").get()
            # 作者
            author = bean.xpath(".//li[@class='article-info']/a/@title").get()
            # 作者头像
            author_portrait = bean.xpath(".//li[@class='article-info']/a/@href").get()
            # 发布时间
            issue_time = bean.xpath(".//li[@class='article-info']/span[1]/text()").get()
            # 访问量
            pageview = bean.xpath(".//li[@class='article-info']/span[2]/text()").get()

            data_dict = {}
            data_dict['title'] = title
            data_dict['detail_url'] = detail_url
            data_dict['introduce'] = str(introduce).replace('\n', '')
            data_dict['author'] = author
            data_dict['author_portrait'] = author_portrait
            data_dict['issue_time'] = issue_time.replace(' · ', '')
            data_dict['pageview'] = pageview
            # print(data_dict)
            data_list.append(data_dict)

        # 数据合并，传递给管道
        for data in data_list:
            detail_url = data['detail_url']
            for img in img_list:
                if detail_url in img["detail_url"]:
                    column_info = {**img, **data}
                    img_list.remove(img)
                    item = ColumnItem()
                    item['id'] = column_info['id']
                    item['title'] = column_info['title']
                    item['detail_url'] = column_info['detail_url']
                    item['introduce'] = column_info['introduce']
                    item['author'] = column_info['author']
                    item['author_portrait'] = column_info['author_portrait']
                    item['issue_time'] = column_info['issue_time']
                    item['pageview'] = column_info['pageview']
                    # 传递给管道
                    yield item
                    # 详情数据：追加爬取的RUL,交给调度器
                    yield scrapy.Request(item['detail_url'], callback=self.parse_detail,
                                         meta={"info": (item['id'], item['issue_time'])})
                    break

        data_list.clear()
        img_list.clear()
        # 更多加载数据
        more_img_temp = response.xpath("//div[@id='custom-load']/ol")
        more_data_temp = response.xpath("//div[@id='custom-load']//ul")

        for bean in more_img_temp:
            id = bean.xpath(".//@data-information-id").get()
            detail_url = bean.xpath(".//a/@href").get().strip()
            img_url = bean.xpath(".//a/img/@src").get().strip()
            img_dict = {}
            img_dict['id'] = id
            img_dict['detail_url'] = detail_url
            img_dict['img_url'] = img_url
            img_list.append(img_dict)

        for bean in more_data_temp:
            title = bean.xpath(".//a/@title").get().strip()
            detail_url = bean.xpath(".//a/@href").get().strip()
            # 简介
            introduce = bean.xpath(".//li/text()").get()
            # 作者
            author = bean.xpath(".//li[@class='article-info']/a/span/text()").get()
            # 作者头像
            author_portrait = bean.xpath(".//li[@class='article-info']/a/img/@src").get()
            # 发布时间
            issue_time = bean.xpath(".//li[@class='article-info']/span[1]/text()").get().replace(' · ', '')
            # 访问量
            pageview = bean.xpath(".//li[@class='article-info']/span[2]/text()").get()

            data_dict = {}
            data_dict['title'] = title
            data_dict['detail_url'] = detail_url
            data_dict['introduce'] = introduce
            data_dict['author'] = author
            data_dict['author_portrait'] = author_portrait
            data_dict['issue_time'] = issue_time
            data_dict['pageview'] = pageview
            data_list.append(data_dict)

        # 数据合并，传递给管道
        for data in data_list:
            detail_url = data['detail_url']
            for img in img_list:
                if detail_url in img["detail_url"]:
                    column_info = {**img, **data}
                    img_list.remove(img)
                    item = ColumnItem()
                    item['id'] = column_info['id']
                    item['title'] = column_info['title']
                    item['detail_url'] = column_info['detail_url']
                    item['introduce'] = column_info['introduce']
                    item['author'] = column_info['author']
                    item['author_portrait'] = column_info['author_portrait']
                    item['issue_time'] = column_info['issue_time']
                    item['pageview'] = column_info['pageview']
                    # 传递给管道
                    yield item

                    # 详情,交给调度器
                    yield scrapy.Request( item['detail_url'], callback=self.parse_detail, meta={"info": (item['id'], item['issue_time'])})

                    break

        # # 追加爬取的RUL,交给调度器
        # if self.run_index < self.run_count:
        #     print("\n\n 开始爬取下一页：" + next_page_url)
        #     yield scrapy.Request(next_page_url, callback=self.parse)

        print("\n\n " + self.name + " parse---------------end")

    ##
    ##
    ##
    # 解析专栏详情
    def parse_detail(self, response):
        print("\n\n " + self.name + " detail---------------start")
        id, issue_time = response.meta.get("info")
        title = response.xpath(".//div[@class='js-article']/div[@class='title']/h2/text()").get()
        content = response.xpath(".//div[@class='js-article']").extract()
        print(content)
        # detail_url = response.xpath(".//div[@class='crumb line22']/span[4]/a/@href").extract()

        # # issue_time = response.xpath(".//div[@class='time gray5 font12']/ul/span[1]/text()").extract()
        # author = response.xpath(".//div[@class='time gray5 font12']/ul/span[2]/a/text()").extract()
        # browse = response.xpath(".//div[@class='time gray5 font12']/ol/span/text()").extract()
        # # 来源
        # source = response.xpath(".//div[@class='time gray5 font12 margin-b10']/ul[1]/span[1]/a/text()").extract()
        # # 责任编辑
        # compile = response.xpath(".//div[@class='time gray5 font12 margin-b10']/ul[1]/span[2]/text()").extract()
        #
        # item = ColumnDetailItem()
        #
        # item['title'] = getStrFirst(title)
        # item['detail_url'] = getStrFirst(detail_url)

        # content = getStrFirst(content)
        # # 去除无效内容
        # trash = '<img src="/ts.jpg">'
        # item['content'] = content.replace(trash, '')
        #
        # item['issue_time'] = getStrFirst(issue_time)
        # item['author'] = getStrFirst(author)
        #
        # item['browse'] = getStrFirst(browse)
        # item['source'] = getStrFirst(source)
        # item['compile'] = getStrFirst(compile)
        #
        # yield item
        # print("detail " + getStrFirst(detail_url) + "  " + getStrFirst(title))
        print("\n\n " + self.name + " detail---------------end")
