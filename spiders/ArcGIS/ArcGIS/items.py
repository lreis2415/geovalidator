# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field

# tool reference
class ArcgisItem(Item):
    # define the fields for your item here like:
    name = Field()
    # summary
    description = Field()
    parameters = Field()
    manual_url = Field()
    example = Field()
    usage = Field()
    syntax = Field()
    pass
