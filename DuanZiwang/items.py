# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class DuanziwangItem(Item):
    url = Field()
    category = Field()
    title = Field()
    author = Field()
    publish_date = Field()
    content = Field()
    read_num = Field()
    comment_num = Field()
    thumb_up_num = Field()
    tags = Field()
