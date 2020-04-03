# -*- coding: utf-8 -*-
import scrapy
from ..items import ArcgisItem
import glob
import re


# arcinfo chm
class ArcgisSpider(scrapy.Spider):
	name = 'arcgis'
	# allowed_domains = ['esri.com']
	# start_urls = ['http://www.esri.com/']
	htmls = glob.glob('H:/OntoBase/egc-materials/arcgis_help/arcinfo_all/*.htm')
	local = "file://127.0.0.1/"
	start = (local + htmls[0]).replace('\\', '/')
	start_urls = [start]

	def parse(self, response):
		for htm in self.htmls[1:]:
			# default callback is parse
			url = (self.local + htm).replace('\\', '/')
			yield scrapy.Request(url=url, callback=self.parse_content)

	def parse_content(self, response):
		item = ArcgisItem()
		syntax = response.css('#content>div.section2[purpose="gptoolsyntax"]>div[purpose="gptoolexpression"]::text').extract_first()
		if syntax is None:
			return
		item['syntax'] = syntax
		name = response.css('#content>div.header>h1::text').extract_first().strip()
		item['name'] = name
		item['description'] = ' '.join(response.css('#content>div.section2[purpose="summary"]>p *::text').extract())
		# item['manual_url'] = response.url
		item['example'] = self.parse_example(response)
		item['usage'] = response.css('#content>div.section2[purpose="gptoolusages"] p *::text').extract()
		item['parameters'] = self.parse_params(response)
		return item

	def parse_params(self, resp):
		tbl = resp.css('#content>div.section2[purpose="gptoolsyntax"]>table.gptoolparamtbl')
		trs = tbl.xpath("./tr")
		params = []
		for tr in trs[1:]:
			param = dict()
			name = tr.xpath("./td[1]/div[1]/text()").extract_first()
			param['name'] = name
			if name and (name.lower().startswith('out_') or name.lower().startswith('output_')):
				param['isOutputFile'] = True
			elif name and (name.lower().startswith('in_') or name.lower().startswith('input_')):
				param['isInputFile'] = True
			optional = tr.xpath("./td[1]/div[2]/text()").extract_first()
			if optional == '(Optional)':
				param['isOptional'] = True
			else:
				param['isOptional'] = False
			param['description'] = self.parse_desc(tr)
			param['dataType'] = tr.xpath('./td[@purpose="gptoolparamtype"]/text()').extract_first()
			params.append(param)
		tbl2 = resp.css('#content>div.section2[purpose="gptoolsyntax"]>.section3[purpose="gptoolretval"]>table.gptoolretvaltbl')
		trs2 = tbl2.xpath("./tr")
		for tr2 in trs2[1:]:
			param = dict()
			name = tr2.xpath('./td[@purpose="gptoolretvalname"]//text()').extract_first()
			if name.lower().startswith('out_') or name.lower().startswith('output_'):
				param['isOutputFile'] = True
			param['name'] = name
			optional = tr2.xpath('./td[@purpose="gptoolretvalname"]/div[2]/text()').extract_first()
			if optional == '(Optional)':
				param['isOptional'] = True
			else:
				param['isOptional'] = False
			param['description'] = self.parse_desc(tr2)
			param['dataType'] = tr2.xpath('./td[@purpose="gptoolparamtype"]/text()').extract_first()
			params.append(param)
		return params

	def parse_desc(self, resp):
		td = resp.xpath('./td[@purpose="gptoolparamdesc"]')
		p = td.xpath('.//p//text()').extract()
		ul = td.xpath('.//ul//li//text()').extract()
		ps = ''
		uls = ''
		if p: ps = ' '.join(p)
		if ul: uls = ' '.join(ul)
		desc = ps + ' ' + uls
		desc = re.sub("(\s){2,}", ' ', desc)
		return desc

	def parse_example(self, resp):
		example = dict()
		# nth-child(2) 表示div.codeblock为父级元素的第二个子元素，不是第二个div.codeblock
		div = resp.css('#content>div.section2[purpose="codesamples"]>div.codeblock:nth-child(2)')
		# print(div)
		example['title'] = div.css('span[purpose="codeblock_title"]::text').extract_first()
		# print(example['title'])
		example['description'] = div.css('div[purpose="codeblockdesc"]>p::text').extract_first()
		code = div.css('div.highlight span::text').extract()
		code_str = ' '.join(code)
		example['code'] = code_str.replace(' . ', '.')
		return example

	def parse_dtype(self, tr):
		dtype = tr.xpath('./td[@purpose="gptoolparamtype"]/text()').extract_first()
		if '|' in dtype:
			dtype.split('|')
		elif ';' in dtype:
			dtype.split(';')
