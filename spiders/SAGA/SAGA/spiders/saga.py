# -*- coding: utf-8 -*-
import scrapy
from ..items import SagaItem
import re


# ta_preprocessor_6
class SagaSpider(scrapy.Spider):
	name = 'saga'
	allowed_domains = ['saga-gis.org']
	start_urls = ['http://www.saga-gis.org/saga_tool_doc/7.3.0/a2z.html']
	base_url = 'http://www.saga-gis.org/saga_tool_doc/7.3.0/'

	def parse(self, response):
		alist = response.xpath('//table//tr[position()>1]/td[1]/a')
		# yield scrapy.Request('http://www.saga-gis.org/saga_tool_doc/7.3.0/pointcloud_tools_10.html', callback=self.parse_content)
		for a in alist:
			next_url = a.css("a::attr(href)").extract_first()
			# skip deprecated and interactive functionalities
			if re.match("\[deprecated\]", a.css("a::text").extract_first()):
				continue
			if '(interactive)' in a.css("a::text").extract_first():
				continue
			yield scrapy.Request(self.base_url + next_url, callback=self.parse_content)

	def parse_content(self, resp):
		item = SagaItem()
		item['manual_url'] = resp.url
		name = resp.xpath("//main/h1/text()").extract_first()
		name = re.sub("^Tool([ 0-9:]+)?", '', name)
		item['name'] = name
		item['description'] = resp.xpath("//main/p//text()").extract()
		# Tool Mass Balance Index
		if ' '.join(item['description']).strip().startswith("References"):
			item['references'] = item['description']
			item['description'] = []
		else:
			item['references'] = self.parse_references(resp)
		item['authors'] = self.parse_authors(resp)
		item['keywords'] = self.parse_keywords(resp)
		item['command'] = self.parse_cmd(resp)
		item['parameters'] = self.parse_parameters(resp)
		return item

	def parse_references(self, resp):
		lis = resp.xpath("//main/ul[preceding::h3[1]/em/text()='References'][1]//li")
		references = [' '.join(li.xpath(".//text()").extract()) for li in lis]
		return references

	def parse_authors(self, resp):
		path = "//main/ul/li[contains(text(),'Author')][1]/text()"
		words = resp.xpath(path).extract_first()
		if words is None:
			return []
		words = words.replace("Author: ", '')
		return re.split("\|", words)

	def parse_keywords(self, resp):
		path = "//main/ul/li[contains(text(),'Menu')][1]/text()"
		words = resp.xpath(path).extract_first()
		if words is None:
			return []
		words = words.replace("Menu: ", '')
		return re.split("\|", words)

	def parse_cmd(self, resp):
		cmd = dict()
		# executable
		cmd['exec'] = resp.xpath("normalize-space(//main/pre[@class='usage']/strong/text())").extract_first()
		# usage
		cmd['cmd_line'] = resp.xpath("normalize-space(//main/pre[@class='usage'])").extract_first().replace('Usage:', '')
		return cmd

	def parse_parameters(self, resp):
		table = resp.xpath("//main//table[last()]")
		trs = table.xpath(".//tr[position()>1]")
		parameter = dict()
		input_trs = []
		output_trs = []
		options_trs = []
		in_rows = 0
		out_rows = 0
		for tr in trs:
			if tr.xpath("./td[1][contains(text(),'Input')]"):
				rows_str = str(tr.xpath("normalize-space(./td[1][contains(text(),'Input')]/@rowspan)").extract_first())
				if rows_str is not None and rows_str != '':
					in_rows = int(rows_str)
					input_trs.extend(trs[:in_rows])
			elif tr.xpath("./td[1][contains(text(),'Output')]"):
				rows_str = str(tr.xpath("normalize-space(./td[1][contains(text(),'Output')]/@rowspan)").extract_first())
				if rows_str is not None and rows_str != '':
					out_rows = int(rows_str)
					output_trs.extend(trs[in_rows:in_rows + out_rows])
			elif tr.xpath("./td[1][contains(text(),'Options')]"):
				options_trs.extend(trs[(in_rows + out_rows):])
		parameter['inputs'] = self.inputs_handler(input_trs)
		parameter['outputs'] = self.outputs_handler(output_trs)
		parameter['options'] = self.options_handler(options_trs)
		return parameter

	def inputs_handler(self, trs):
		inputs = []
		for tr in trs:
			input_param = dict()
			optional = False
			i = 0
			if tr.xpath("./td[1][normalize-space(@class)='labelSection']"):
				i = 1
			name = tr.xpath("./td[" + str(i + 1) + "]/text()").extract_first()
			input_param['name'] = name
			input_param['isInputFile'] = True
			if str(name).endswith('(*)'):
				optional = True
			input_param['isOptional'] = optional
			input_param['dataType'] = self.type_handler(tr, i + 2)
			input_param['flag'] = tr.xpath("./td[" + str(i + 3) + "]/code/text()").extract_first()
			if name is None:
				input_param['name'] = input_param['flag']
			des = tr.xpath("./td[" + str(i + 4) + "]/text()").extract_first()
			if des is not None:
				des = des.replace('"-"', "")
			input_param['description'] = des
			input_param['constraints'] = self.constraints_handler(tr, i + 5)
			inputs.append(input_param)
		return inputs

	def outputs_handler(self, trs):
		outputs = []
		for tr in trs:
			output = dict()
			optional = False
			i = 0
			if tr.xpath("./td[1][normalize-space(@class)='labelSection']"):
				i = 1
			name = tr.xpath("./td[" + str(i + 1) + "]/text()").extract_first()
			output['name'] = name
			output['isOutputFile'] = True
			if str(name).endswith('(*)'):
				optional = True
			output['isOptional'] = optional
			output['type'] = self.type_handler(tr, i + 2)
			output['flag'] = tr.xpath("./td[" + str(i + 3) + "]/code/text()").extract_first()
			if name is None:
				output['name'] = output['flag']
			des = tr.xpath("./td[" + str(i + 4) + "]/text()").extract_first()
			if des is not None:
				des = des.replace('"-"', "")
			output['description'] = des
			output['constraints'] = self.constraints_handler(tr, i + 5)
			outputs.append(output)
		return outputs

	def options_handler(self, trs):
		options = []
		# bugs 有问题
		for tr in trs:
			option = dict()
			i = 0
			if tr.xpath("./td[1][normalize-space(@class)='labelSection']"):
				i = 1
			name = tr.xpath("./td[" + str(i + 1) + "]/text()").extract_first()
			if name == '(*) optional':
				continue
			option['name'] = name
			option['dataType'] = self.type_handler(tr, i + 2)
			option['flag'] = tr.xpath("./td[" + str(i + 3) + "]/code/text()").extract_first()
			if name is None:
				option['name'] = option['flag']
			description = tr.xpath("./td[" + str(i + 4) + "]/text()").extract_first()
			if description is not None:
				description.strip().replace('-', "")
			option['description'] = description
			option['constraints'] = self.constraints_handler(tr, i + 5)
			# print(option)
			options.append(option)
		return options

	def type_handler(self, tr, i):
		val_type = tr.xpath("./td[" + str(i) + "]/text()").extract_first()
		if str(val_type).endswith("(input)"):
			return str(val_type).replace("(input)", '')
		elif str(val_type).endswith("(optional output)"):
			return str(val_type).replace("(optional output)", '')
		elif str(val_type).endswith("(output)"):
			return str(val_type).replace("(output)", '')
		else:
			return val_type

	def constraints_handler(self, tr, i):
		constraints = dict()
		# normalize-space 只能够处理一个结点，不能处理节点集，即无法处理 //text()
		constraints_str = ' '.join(tr.xpath("./td[" + str(i) + "]//text()").extract()).strip()
		constraints_str = constraints_str.replace('-', '')
		# print('constraints_str %s' % constraints_str)
		if constraints_str is None or constraints_str == '':
			return None
		min_val = re.search("Minimum: \d+\.\d+", constraints_str)
		if min_val is not None:
			constraints['minimum'] = min_val.group().replace("Minimum: ", '')
		# print(constraints['minimum'])
		max_val = re.search("Maximum: \d+\.\d+", constraints_str)
		if max_val is not None:
			constraints['maximum'] = max_val.group().replace("Maximum: ", '')
		# print(constraints['maximum'])
		default_val = re.search("Default: [\w\.]+", constraints_str)
		if default_val is not None:
			constraints['defaultValue'] = default_val.group().replace("Default: ", '')
		# print(constraints['default'])
		available_choices = re.search("Available Choices: [\[\]\w()% -]+[Default:]?", constraints_str)
		availableChoices = []
		if available_choices is not None:
			choices_str = available_choices.group().replace("Default:", '')
			choices_list = re.findall("\[[0-9]\][ a-zA-Z-]+", choices_str)
			for l in choices_list:
				choices = dict()
				choice = re.search("(?<=\[)[0-9]", l).group()
				des = re.search("[a-zA-Z -]+", l).group()
				choices['choice'] = choice
				choices['description'] = des
				availableChoices.append(choices)
			constraints['availableChoices'] = availableChoices
		parameters = re.search("^\d+ Parameters:", constraints_str)
		if parameters is not None:
			constraints['parameters_des'] = constraints_str
		fields = re.search("^\d+ Fields:", constraints_str)
		if fields is not None:
			constraints['fields_des'] = constraints_str
		return constraints
