# -*- coding: utf-8 -*-
import scrapy
from ..items import DyspiderItem
class DySpider(scrapy.Spider):
    name = 'dy'
    # allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.ygdy8.net/html/gndy/dyzz/index.html']


    def parse(self, response):
        # total_page = response.xpath('//select[@name="sldd"]/option[last()]/text()').extract()[0]
        total_page = response.xpath('//select[@name="sldd"]/option[last()]/text()').extract_first()
        for x in range(1, int(total_page) + 1):
            # 根据x的值，拼接完整页面url地址
            url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_%s.html' % x

            yield scrapy.Request(
                url=url,
                callback=self.parse_list
            )
    def parse_list(self, response):
            # 4.使用xpath查找所有的href属性值
            hrefs = response.xpath('//a[@class="ulink"]/@href').extract()
            # for循环取出所有的href值
            for href in hrefs:
                # print('正在爬取第%s个电影信息..'%count)
                # 拼接完整的url地址
                detail_url = 'http://www.ygdy8.net%s' % href
                # 发送请求，拿回详情页面的数据
                yield scrapy.Request(
                    url=detail_url,
                    callback=self.parse_detail
                )

    def parse_detail(self, response):
        # 根据xpath从详情页提取数据
        movie_info = response.xpath('//div[@id="Zoom"]//text()').extract()
        # for中存放的就是电影的所有信息
        for movie in movie_info:
            if u'译　　名' in movie:
                movie_name = movie.split(u'　')[-1]
            elif u'类　　别' in movie:
                movie_type = movie.split(u'　')[-1]
            elif u'片　　长' in movie:
                movie_time = movie.split(u'　')[-1]
            elif u'导　　演' in movie:
                directors = movie.split(u'　')[-1]
            elif u'主　　演' in movie:
                actors = movie.split(u'　')[-1]
        download_url = response.xpath('//tbody/tr/td/a/@href').extract_first()
        if download_url:
            if download_url[0][0]!='m':
                item = DyspiderItem()
                item['m_name'] = movie_name
                item['m_type'] = movie_type
                item['m_time'] = movie_time
                item['directors'] = directors
                item['actors'] = actors
                item['m_url'] = download_url
                yield item


