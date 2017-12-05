# -*- coding: utf-8 -*-
import scrapy
from DuanZiwang.items import DuanziwangItem


class DuanziSpider(scrapy.Spider):
    name = 'duanzi'
    allowed_domains = ['duanziwang.com']
    # start_urls = ['http://duanziwang.com/']

    def start_requests(self):
        base_url = 'http://duanziwang.com/page/{page_num}'  # 这里base_url和 url不要同名， 因为在循环一次后，url就变成一个固定的值，再去format就无意义
        for page_num in range(1,101):
            url = base_url.format(page_num=page_num)
            # self.logger.debug("testing %s" %url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        解析源码，获取其中的数据
        获取下一页链接，再解析源码
        :param response: 
        :return: 
        """
        article_nodes = response.xpath('//article[@class="excerpt"]')
        for node in article_nodes:
            category = node.xpath(".//a[contains(@class, 'cat')]/text()").extract_first("")
            url = node.xpath(".//h2/a/@href").extract_first("")
            title = node.xpath(".//h2/a/text()").extract_first("")
            author = node.xpath(".//p[@class='text-muted time']/text()").re("(.*?)发布于(.*)")[0].strip()
            publish_date = node.xpath(".//p[@class='text-muted time']/text()").re("(.*?)发布于(.*)")[1].strip()
            content = node.xpath(".//p[@class='note']").extract_first("")
            read_num = node.xpath(".//span[@class='post-views']/text()").re("阅读\((\d+)\)")[0]
            comment_num = node.xpath(".//span[@class='post-comments']/text()").re("评论\((\d+)\)")[0]
            thumb_up_num = node.xpath(".//a[@class='post-like']/span/text()").extract_first('')
            tags = ",".join(node.xpath(".//span[@class='post-tags']/a/text()").extract())
            duanzi_item = DuanziwangItem()
            for field in duanzi_item.fields:
                # self.logger.debug("测试field： %s, type: %s" %(field, type(field)))   # 类型为str
                duanzi_item[field] = eval(field)

            yield duanzi_item


