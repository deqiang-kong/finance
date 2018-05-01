import scrapy
from scrapy.spiders import CrawlSpider

from finance.util.timeutil import getTimeConversion
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
            data_dict['author_portrait'] = 'http://www.jinse.com/' + author_portrait
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
                    item['img_url'] = column_info['img_url']
                    item['detail_url'] = column_info['detail_url']
                    item['introduce'] = column_info['introduce']
                    item['author'] = column_info['author']
                    item['author_portrait'] = column_info['author_portrait']
                    item['issue_time'] = getTimeConversion(column_info['issue_time'])
                    item['pageview'] = column_info['pageview']
                    # 传递给管道
                    yield item
                    # 详情数据：追加爬取的RUL,交给调度器
                    yield scrapy.Request(item['detail_url'], callback=self.parse_detail,
                                         meta={"info": (item['id'], item['title'], item['issue_time'])})
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
            data_dict['issue_time'] = getTimeConversion(issue_time)
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
                    item['img_url'] = column_info['img_url']
                    item['detail_url'] = column_info['detail_url']
                    item['introduce'] = column_info['introduce']
                    item['author'] = column_info['author']
                    item['author_portrait'] = column_info['author_portrait']
                    item['issue_time'] = getTimeConversion(column_info['issue_time'])
                    item['pageview'] = column_info['pageview']
                    # 传递给管道
                    yield item

                    # 详情,交给调度器
                    yield scrapy.Request(item['detail_url'], callback=self.parse_detail,
                                         meta={"info": (item['id'], item['title'], item['issue_time'])})

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
        id, title, issue_time = response.meta.get("info")

        source = response.xpath(".//div[@class='js-article']")
        content = response.xpath(".//div[@class='js-article']").get()

        title_info = source.xpath(".//div[@class='title']").get()
        article_info = source.xpath(".//div[@class='article-info']").get()
        # 实时btc价格
        btc_price = source.xpath(".//div[@class='btc-price']").get()
        # 广告
        ad_list = source.xpath(".//div[@class='ad-list']").get()

        # 去除无效内容
        content = str(content).replace(title_info, "")
        content = str(content).replace(article_info, "")
        content = str(content).replace(ad_list, "")
        content = str(content).replace(btc_price, "")
        trash = '<img src="/ts.jpg">'
        content = content.replace(trash, '')
        # print(content)

        item = ColumnDetailItem()
        item['id'] = id
        item['title'] = title
        item['content'] = content
        item['issue_time'] = issue_time
        yield item
        print("\n\n " + self.name + " detail---------------end")
