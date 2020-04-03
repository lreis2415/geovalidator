# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class SagaItem(Item):
	name = Field()
	# comment
	description = Field()
	parameters = Field()
	# exec and cmd line (syntax)
	command = Field()
	manual_url = Field()
	keywords = Field()
	authors = Field()
	references = Field()
	pass
