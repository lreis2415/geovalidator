#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/3 16:04

from owlready2 import *
import json
import re
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils
from JSON2OWL.OwlConvert.Preprocessor import Preprocessor
from rdflib import BNode, RDF, Graph, URIRef, Namespace, Literal
from rdflib.collection import Collection

module_uri = 'http://www.egc.org/ont/process/saga'
onto = get_ontology(module_uri)
# onto, skos, dcterms, props = OWLUtils.load_common(onto)
onto, sh, skos, dcterms, props, foaf = OWLUtils.load_common(onto)
onto, geospatial = OWLUtils.load_geo_vocabl(onto)
onto, gb, task, data, cyber, context = OWLUtils.load_common_for_process_tool(onto)
# rdf namespaces
Data, Cyber, Skos, Sh, Geo, Sf, Process = OWLUtils.rdfnamespaces()

print('ontologies imported')

# sh:declare
# TODO TEST
# OWLUtils.declear_prefix('ns_saga', onto)

with onto:
	# print(gb.GeoprocessingFunctionality)

	class SagaTool(gb.GeoprocessingFunctionality):
		pass


	class SagaInput(cyber.Input):
		pass


	class SagaOutput(cyber.Output):
		pass


	class SagaOption(cyber.Option):
		pass


	# class SagaConstraint(gb.Constraint):
	# 	pass

	class SagaAvailableChoice(cyber.AvailableChoice):
		pass

onto.metadata.creator.append('houzhiwei')
onto.metadata.title.append('SAGA GIS')
onto.metadata.versionInfo.append('7.3.0')
import datetime

onto.metadata.created.append(datetime.datetime.today())

g = default_world.as_rdflib_graph()

def get_property(option, prop_type):
	"""
		根据配置查找对应的属性，没有则创建新的属性

	Args:
		option: property name
		prop_type: ObjectProperty or DataProperty

	Returns: created property name

	"""
	config = OWLUtils.get_config(module_path + '/config.ini')
	_prop = OWLUtils.get_option(config, 'saga', option)
	if _prop is None:
		if onto.__getattr__(option) is None:
			OWLUtils.create_onto_class(onto, option, prop_type)
		return option
	else:
		return _prop


def get_format(option):
	"""对应的数据格式"""
	config = OWLUtils.get_config(module_path + '/config.ini')
	_prop = OWLUtils.get_option(config, 'format', option)
	return _prop


def handle_inout(tool, item_value, in_or_out):
	for ioD in item_value:
		# print(ioD)
		io_name = ioD['name']
		if io_name is None:
			io_name = in_or_out
		_name = Preprocessor.io_name(io_name, onto)
		param_rdf = None
		if in_or_out == 'input':
			param = SagaInput(_name, prefLabel=locstr(io_name, lang='en'))
			# param = SagaInput(0,prefLabel=locstr(io_name, lang='en')) # blank node prefix with _:
			tool.input.append(param)
			param.isInput = True
			# rdflib
			param_rdf = URIRef(param.iri)
			with onto:
				g.add((param_rdf, RDF.type, Sh.NodeShape))
				g.add((param_rdf, RDF.type, URIRef(SagaInput.iri)))
		else:
			param = SagaOutput(_name, prefLabel=locstr(io_name, lang='en'))
			# param =SagaOutput(0, prefLabel=locstr(io_name, lang='en'))
			tool.output.append(param)
			param.isOutput = True
			# rdflib
			param_rdf = URIRef(param.iri)
			with onto:
				g.add((param_rdf, RDF.type, Sh.NodeShape))
				g.add((param_rdf, RDF.type, URIRef(SagaOutput.iri)))

		if ioD['dataType']:
			vr = re.match("[a-zA-Z ]+ (?=\([a-zA-Z ]+\))?", ioD['dataType'])
			dformat = vr.group().strip()
			if not get_format(dformat):
				continue
			param.supportsDataFormat.append(data[get_format(dformat)])
			# rdflib
			formatshape = g.BNode()
			with onto:
				g.add((param_rdf, Sh.property, formatshape))
				g.add((formatshape, RDF.type, Sh.PropertyShape))
				g.add((formatshape, Sh.path, Cyber.supportsDataFormat))
			formats = g.BNode()
			with onto:
				g.add((formats, RDF.first, [data[get_format(dformat)]]))
				g.add((formats, RDF.rest, RDF.nil))
				c = Collection(g, formats)
				g.add((formatshape, Sh['in'], c))

		param.identifier = ioD['name']
		param.description.append(ioD['description'])
		param.flag = ioD['flag']
		param.isOptional = ioD['isOptional']
		OWLUtils.link_to_domain_concept(param, io_name.replace('_', ' '))
		# shacl
		pshape = Sh.PropertyShape(0)
		pshape.path = onto.dataContent
		if not ioD['isOptional']:
			pshape.minCount = 1
			pshape.message.append(ioD['name'] + " is required!")


def handle_options(tool, option, _onto):
	name = option['name']
	if name is None:
		name = 'option'
	_name = Preprocessor.io_name(Preprocessor.name_underline(name), _onto)
	op = SagaOption(_name, prefLabel=locstr(name, lang='en'))
	tool.option.append(op)
	if option['description'] != '-':
		op.description = option['description']
	op.flag = option['flag']
	op.identifier = name
	constraints = option['constraints']
	# shacl
	pshape = Sh.PropertyShape(0)
	pshape.path.append(_onto.dataContent)
	if constraints:
		if 'fields_des' in constraints.keys() and constraints['fields_des']:
			op.description.append(constraints['fields_des'])
		else:
			if 'minimum' in constraints.keys() and constraints['minimum']:
				op.minimum = constraints['minimum']
				pshape.minExclusive = constraints['minimum']
			if 'defaultValue' in constraints.keys() and constraints['defaultValue']:
				op.defaultValue = constraints['defaultValue']
				pshape.defaultValue = constraints['defaultValue']
			if 'maximum' in constraints.keys() and constraints['maximum']:
				op.maximum = constraints['maximum']
				pshape.maxInclusive = constraints['maximum']
			op.datatypeInString.append(option['dataType'])
			pshape.datatype = [OWLUtils.get_datatype_iris(option['dataType'])]
			op.datatype.append(OWLUtils.get_datatype_iris(option['dataType']))
			if 'availableChoices' in constraints.keys() and constraints['availableChoices']:
				c = []
				for achoice in constraints['availableChoices']:
					c.append(achoice['choice'])
				with _onto:
					g.add((pshape, Sh['in'], c))
				OWLUtils.handle_choices(op, name, constraints['availableChoices'], SagaAvailableChoice, _onto)


def handle_task(tool, tool_name, en_str, _keywords, desc):
	config = OWLUtils.get_config(module_path + '/config.ini')
	tasks = config.options('task')
	for task_item in tasks:
		# print(task_item)
		if task_item in _keywords:
			task_cls = config.get('task', task_item)
			task_name = Preprocessor.task_name(tool_name)
			if task[task_name] is None:
				task_ins = task[task_cls](task_name, prefLabel=locstr(en_str.replace('Tool', '') + " task", lang='en'))
				# task_ins = task[task_cls](tool_name + "_task", prefLabel=locstr(en_str.replace('Tool', '') + " task", lang='en'))
				task_ins.description.append(locstr(desc, lang='en'))
				task_ins.isAtomicTask = True
				task_ins.identifier = task_name
			else:
				task_ins = task[task_name]
			if (task_ins in tool.usedByTask) is False:
				tool.usedByTask.append(task_ins)
			if (tool in tool.processingTool) is False:
				task_ins.processingTool.append(tool)


# TODO TEST
def handle_similar_tools(tool, tool_label):
	"""link tools which have the same names"""
	clean_tool_label = Preprocessor.remove_bracket_content(tool_label)
	similars = onto.search(prefLabel=clean_tool_label + '*')
	if len(similars) > 0:
		for similar in similars:
			if clean_tool_label == Preprocessor.remove_bracket_content(similar.prefLabel[0]):
				tool.closeMatch.append(similar)
				similar.closeMatch.append(tool)


def map_to_owl(json_data):
	for d in json_data:
		"""mapping json data to ontology properties"""
		name = Preprocessor.toolname_underline(d['name'])
		# name = re.sub("[()-*,/]", " ", name).strip()
		executable = Preprocessor.normalize("saga_cmd ", d['command']['exec'])
		keywords = d['keywords']
		toolClass = tool_class(keywords)
		if onto[name]:
			# if has the same name and executable
			if onto[name].executable == executable:
				onto[name].is_a.append(toolClass)
				continue
			else:
				name = name + '_' + keywords[0].replace(' ', '_')
		tool = toolClass(name, prefLabel=locstr(re.sub('^(Tool)[0-9: ]+', '', d['name']), lang='en'))
		# tool = toolClass(Preprocessor.space_2_underline(name), prefLabel=locstr(re.sub('^(Tool)[0-9: ]+', '', d['name']), lang='en'))
		tool.isToolOfSoftware.append(cyber.SAGA_GIS)
		tool.identifier = name
		tool.manualPageURL.append(d['manual_url'])
		# task
		handle_task(tool, name, d['name'], keywords, OWLUtils.join_list(d['description']))
		tool.executable = executable
		tool.commandLine.append(Preprocessor.normalize("Usage: ", d['command']['cmd_line']))
		tool.authors.append(OWLUtils.join_keywords(d['authors']))
		for reference in d['references']:
			tool.references.append(reference)
		# keywords
		keywords.append(name.replace('_', ' '))
		OWLUtils.link_to_domain_concept(tool, keywords)

		# applicaiton category
		OWLUtils.application_category(tool, [d['keywords'][0]], d['keywords'][1], d['keywords'][2:])

		tool.description.append(OWLUtils.join_list(d['description']))
		if d['parameters']:
			for item, itemValue in d['parameters'].items():
				if item == 'inputs':
					handle_inout(tool, itemValue, 'input')
				elif item == 'outputs':
					handle_inout(tool, itemValue, 'output')
				elif item == 'options':
					for optionItem in itemValue:
						handle_options(tool, optionItem, onto)


def tool_class(keywords):
	tool_cls = keywords[0].replace(' ', '') + 'Tool'
	return OWLUtils.create_onto_class(onto, tool_cls, SagaTool)


if __name__ == "__main__":
	module_path = os.path.dirname(__file__)
	with open(module_path + '/saga.json', 'r') as f:
		jdata = json.load(f)  # list
	# print(len(jdata))
	# otherwise will report stack overflow exception
	size = 1024 * 1024 * 1024 * 20  # related to system
	threading.stack_size(size)
	thread = threading.Thread(target=map_to_owl(jdata))
	thread.start()
	g.serialize('saga.ttl',format='turtle')
	# onto.save(file='saga.owl', format="rdfxml")
	# update task ontology
	task.save()
	print('SAGA Done!')
