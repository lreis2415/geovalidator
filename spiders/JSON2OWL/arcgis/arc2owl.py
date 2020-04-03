#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/7 22:25

from owlready2 import *
import json
import re
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils
from JSON2OWL.OwlConvert.Preprocessor import Preprocessor
import datetime

# import math

module_uri = 'http://www.egc.org/ont/process/arcgis'
onto = get_ontology(module_uri)
# onto, skos, dcterms, props = OWLUtils.load_common(onto)
onto, shacl, skos, dcterms, props, foaf = OWLUtils.load_common(onto)
onto, geospatial = OWLUtils.load_geo_vocabl(onto)
onto, gb, task, data, cyber, context = OWLUtils.load_common_for_process_tool(onto)
print('ontologies imported')

with onto:
	class ArcGISTool(gb.GeoprocessingFunctionality):
		pass


	class ArcGISInput(cyber.Input):
		pass


	class ArcGISOutput(cyber.Output):
		pass


	class ArcGISOption(cyber.Option):
		pass

onto.metadata.creator.append('houzhiwei')
onto.metadata.title.append('ArcGIS Tools')

onto.metadata.created.append(datetime.datetime.today())
module_path = os.path.dirname(__file__)
onto.metadata.versionInfo.append('10.1')


def get_task_type(full_name):
	task_type_partten = "\([a-zA-Z0-9*\-' ]+\)"
	task_types = re.findall(task_type_partten, full_name)

	if len(task_types) > 1:
		# tool.hasKeywords.append(OWLUtils.remove_parenthesis(task_types[0]))
		task_type = Preprocessor.remove_parenthesis(re.findall(task_type_partten, full_name)[-1])
	else:
		task_type = Preprocessor.remove_parenthesis(re.findall(task_type_partten, full_name)[0])
	return task_type


def handle_task(tool, full_name, task_name, des):
	config = OWLUtils.get_config(module_path + '/config.ini')
	task_type = get_task_type(full_name)
	task_cls = config.get('task', task_type)
	# tool.keywords.append(task_type)
	tool.subject.append(task_type)
	# avoid duplicate
	if not task[task_name + "_task"]:
		task_ins = task[task_cls](task_name + "_task", prefLabel=locstr(task_name.replace('_', ' ') + " task", lang='en'))
		task_ins.isAtomicTask = True
		task_ins.identifier = task_name
	else:
		task_ins = task[task_name + "_task"]
	if (task_ins in tool.usedByTask) is False:
		tool.usedByTask.append(task_ins)
	if (tool in tool.processingTool) is False:
		task_ins.processingTool.append(tool)
	task_ins.description.append(locstr(des, lang='en'))


def handle_parameters(tool, param):
	# 部分parameter不包含isInputFile等属性
	_name = Preprocessor.io_name(param['name'], onto)
	if 'isInputFile' in param.keys() and param['isInputFile']:
		p = ArcGISInput(_name, prefLabel=locstr(param['name'], lang='en'))
		# p = ArcGISInput(0, prefLabel=locstr(param['name'], lang='en'))
		tool.input.append(p)
		p.isInput = param['isInputFile']
		OWLUtils.link_to_domain_concept(p, param['name'].replace('_', ' '))
	elif 'isOutputFile' in param.keys() and param['isOutputFile']:
		p = ArcGISOutput(_name, prefLabel=locstr(param['name'], lang='en'))
		# p = ArcGISOutput(0, prefLabel=locstr(param['name'], lang='en'))
		tool.output.append(p)
		p.isOutput = param['isOutputFile']
		OWLUtils.link_to_domain_concept(p, param['name'].replace('_', ' '))
	else:
		p = ArcGISOption(_name, prefLabel=locstr(param['name'], lang='en'))
		# p = ArcGISOption(0, prefLabel=locstr(param['name'], lang='en'))
		tool.option.append(p)
		dt = param['dataType']
		if dt:
			p.datatypeInString.append(param['dataType'])
			p.datatype.append(OWLUtils.get_datatype_iris(param['dataType']))
		OWLUtils.link_to_domain_concept(p, param['name'].replace('_', ' '))
	p.identifier = param['name']
	p.flag = param['name']
	if 'dataType' in param.keys() and param['dataType']:
		p.datatypeInString.append(param['dataType'])
	p.description.append(param['description'])
	p.isOptional = param['isOptional']
	# datatype
	datatype = param['dataType']
	if datatype is None: datatype = "string"
	dt = datatype.strip().lower().replace(' ', '_')
	# print(dt)
	dtype = data[dt]
	if dtype is None: dtype = OWLUtils.get_datatype_iris(dt)
	p.datatype.append(dtype)
	if "available_values" in param.keys():
		for value in param['available_values']:
			p.availableValue.append(value)

def handle_example(example):
	ex = 'Title: ' + example['title'] if example['title'] else ''
	ex = ex + '\n' + 'Description: ' + example['description'] if example['description'] else ex
	ex += '\n' + 'Code: \n' + example['code']
	return ex


def map_to_owl(json_data):
	for d in json_data:
		"""mapping json data to ontology properties"""
		name = re.match("[0-9a-zA-Z\-/* ]+ (?=\([\w' ]+\))", d['name'])  # 存在同名冲突
		if name:
			name_str = name.group().strip().lower().replace(' ', '_').replace('/', '_')
		else:
			continue
		category = get_task_type(d['name'])
		toolCls = tool_class(category)
		# if already exists a instance has the same name
		if onto[name_str]:
			# if is the same
			if onto[name_str].syntax == d['syntax']:
				onto[name_str].is_a.append(toolCls)
				continue
			else:
				name_str = name_str + '_' + category.lower().replace(' ', '_')
		tool = toolCls(name_str, prefLabel=locstr(name_str.replace('_', ' '), lang='en'))

		keywords = [name_str.replace('_', ' ')]
		OWLUtils.link_to_domain_concept(tool, keywords)

		tool.isToolOfSoftware.append(cyber.ArcGIS_Desktop)
		tool.identifier = name_str.replace('_', ' ')
		# tool.hasManualPageURL.append(d['manual_url'])
		tool.description.append(locstr(d['description'], lang='en'))
		tool.usage.append(OWLUtils.join_list(d['usage']))
		tool.syntax.append(d['syntax'])
		tool.example.append(handle_example(d['example']))
		handle_task(tool, d['name'], name_str, d['description'])
		for parameter in d['parameters']:
			handle_parameters(tool, parameter)


def tool_class(category):
	if category == '3D Analyst': category = 'ThreeDimensionalAnalyst'
	tool_cls = category.replace(' ', '') + 'Tool'
	return OWLUtils.create_onto_class(onto, tool_cls, ArcGISTool)


if __name__ == "__main__":
	with open(module_path + '/arcgis.json', 'r') as f:
		jdata = json.load(f)  # list
	# length = len(jdata)
	# otherwise will report stack overflow exception
	size = 1024 * 1024 * 1024  # 该值与具体的系统相关
	threading.stack_size(size)
	thread = threading.Thread(target=map_to_owl(jdata))
	thread.start()
	onto.save(file='arcgis.owl', format="rdfxml")
	# update task ontology
	task.save()
	print('ArcGIS Done!')
