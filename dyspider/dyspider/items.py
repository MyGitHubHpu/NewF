# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    m_name = scrapy.Field()
    m_type = scrapy.Field()
    m_time = scrapy.Field()
    directors = scrapy.Field()
    actors = scrapy.Field()
    m_url = scrapy.Field()
