#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/2 11:33
from owlready2 import *
from configparser import ConfigParser, NoOptionError
from os import path
from gensim.summarization import keywords
import inspect
from .Preprocessor import Preprocessor
from nltk.corpus import stopwords
from rdflib import BNode, RDF, Graph, URIRef, Namespace, Literal
from rdflib.collection import Collection

class OWLUtils(object):

	@staticmethod
	def curr_path(file_path):
		# print('file://' + path.normpath(path.dirname(__file__) + file_path))
		return 'file://' + path.normpath(path.dirname(__file__) + file_path)

	@staticmethod
	def load_common(onto: Ontology):
		"""
		load skos, dcterms and UniProps into target ontology

		Args:
			onto: Ontology which needs to import ontologies like skos

		Returns: Ontology with imported ontologies
		"""
		onto_path.append(path.normpath(path.dirname(__file__)) + '/')
		# 加入**shacl**会导致无法推理，报 shacl 的namespace值不是 anyURI类型 （？）
		shacl = get_ontology('/shacl.rdf').load(only_local=True)
		skos = get_ontology('/skos.rdf').load(only_local=True)
		dcterms = get_ontology('/dcterms.rdf').load(only_local=True)
		props = get_ontology('/UniProps.owl').load(only_local=True)
		onto.imported_ontologies.append(shacl)
		foaf = get_ontology('/FOAF.rdf').load(only_local=True)
		onto.imported_ontologies.append(foaf)
		onto.imported_ontologies.append(props)
		onto.imported_ontologies.append(skos)
		onto.imported_ontologies.append(dcterms)
		# return onto, skos, dcterms, props
		return onto, shacl, skos, dcterms, props, foaf

	@staticmethod
	def load_foaf(onto: Ontology):
		onto_path.append(path.normpath(path.dirname(__file__)) + '/')
		foaf = get_ontology('/FOAF.rdf').load(only_local=True)
		onto.imported_ontologies.append(foaf)
		return onto, foaf

	@staticmethod
	def load_context(onto: Ontology):
		onto_path.append(path.normpath(path.dirname(__file__)) + '/')
		context = get_ontology('/application-context.owl').load(only_local=True)
		onto.imported_ontologies.append(context)
		return onto, context

	@staticmethod
	def load_datasource(onto: Ontology):
		onto_path.append(path.normpath(path.dirname(__file__)) + '/')
		datasource = get_ontology('/datasource.owl').load(only_local=True)
		onto.imported_ontologies.append(datasource)
		return onto, datasource

	@staticmethod
	def load_geospatial():
		onto_path.append(path.normpath(path.dirname(__file__)) + '/domain/')
		geometry = get_ontology('/geometry.owl').load(only_local=True)
		gcmd = get_ontology('/gcmd_keywords.owl').load(only_local=True)
		csdms = get_ontology('/csdms-standard-names.owl').load(only_local=True)
		# dta = get_ontology('/digital_terrain_analysis.owl').load(only_local=True)
		cf = get_ontology('/cf-standard-names.owl').load(only_local=True)
		# hydrology = get_ontology('/hydrology.owl').load(only_local=True)
		# gis_vocab = get_ontology('/gis_vocab.rdf').load(only_local=True)
		geospatial = get_ontology('/geospatial_vocab_all.owl').load(only_local=True)
		return geospatial

	@staticmethod
	def load_geo_vocabl(onto):
		"""
		load domain ontologies, geospatial imports gcmd, csdms, cf, dta, hydrology, gis_vocab
		Args:
			onto: Ontology
		Returns:
			onto
		"""
		geospatial = OWLUtils.load_geospatial()
		onto.imported_ontologies.append(geospatial)
		return onto, geospatial

	@staticmethod
	def get_vocab_namespace(onto):
		# gcmd = onto.get_namespace('http://www.egc.org/ont/domain/gcmd')
		# csdms = onto.get_namespace("http://www.egc.org/ont/vocab/csdms")
		# cf = onto.get_namespace("http://www.egc.org/ont/vocab/cf")
		# dta = onto.get_namespace("http://www.egc.org/ont/domain/dta")
		# hydrology = onto.get_namespace("http://www.egc.org/ont/domain/hydrology")
		# gis_vocab = onto.get_namespace("http://www.egc.org/ont/vocab/gis")
		geospatial = onto.get_namespace("http://www.egc.org/ont/domain/geospatial")
		# return gcmd, csdms, cf, dta, hydrology, gis_vocab
		return geospatial

	@staticmethod
	def rdfnamespaces():
		Data = Namespace('http://www.egc.org/ont/data#')
		Cyber = Namespace('http://www.egc.org/ont/gis/cyber#')
		Skos = Namespace('http://www.w3.org/2004/02/skos/core#')
		Sh = Namespace('http://www.w3.org/ns/shacl#')
		Geo = Namespace('http://www.opengis.net/ont/geosparql#')
		Sf = Namespace('http://www.opengis.net/ont/sf')
		Process = Namespace('http://www.egc.org/ont/gis/process#')
		return Data, Cyber, Skos, Sh, Geo, Sf, Process

	@staticmethod
	def load_data_soft(onto: Ontology):
		cyber = get_ontology('/gis-soft.owl').load(only_local=True)
		data = get_ontology('/data.owl').load(only_local=True)
		onto.imported_ontologies.append(cyber)
		onto.imported_ontologies.append(data)
		return onto, data, cyber

	@staticmethod
	def load_common_for_process_tool(onto: Ontology):
		geosparql = get_ontology('/geosparql_vocab_all.rdf').load(only_local=True)
		cyber = get_ontology('/gis-soft.owl').load(only_local=True)
		data = get_ontology('/data.owl').load(only_local=True)
		context = get_ontology('/application-context.owl').load(only_local=True)
		gb = get_ontology('/gis-process.owl').load(only_local=True)
		task = get_ontology('/task.owl').load(only_local=True)
		onto.imported_ontologies.append(gb)
		onto.imported_ontologies.append(task)
		onto.imported_ontologies.append(data)
		onto.imported_ontologies.append(context)
		onto.imported_ontologies.append(geosparql)
		return onto, gb, task, data, cyber, context

	@staticmethod
	def set_data_property(obj, dataProp, value):
		"""
		set data property, handle FunctionalProperty
		Args:
			obj: tool or param object
			dataProp: data property string
			value: value

		Returns:
			obj
		"""
		try:
			# not functional Property cannot assign directly (use .append() or assign a list).
			setattr(obj, dataProp, value)
		# obj.__setattr__(dataProp, value)
		except ValueError:  # AttributeError
			# setattr(obj, dataProp, list(value))
			obj.__getattr__(dataProp).append(value)
		return obj

	@staticmethod
	def create_onto_class(onto: Ontology, name, parent_class):
		with onto:
			clazz = types.new_class(name, (parent_class,))
		return clazz

	@staticmethod
	def get_config(ini):
		"""
		使用自定义的OwlConfigerParser
		Args:
			ini: ini 配置文件

		Returns:

		"""
		config = ConfigParser()
		# 保留大小写不变
		# https://stackoverflow.com/questions/1611799/preserve-case-in-configparser
		config.optionxform = str
		config.read(ini, encoding='utf-8')
		return config

	@staticmethod
	def get_option(config, section, option):
		try:
			return config.get(section, option)
		except NoOptionError:
			return None

	@staticmethod
	def join_keywords(list_keywords: list):
		return ', '.join(list_keywords)

	@staticmethod
	def join_list(liststr: list):
		return ' '.join(liststr)

	@staticmethod
	def declear_prefix(prefix, onto):
		o = Thing(onto.ontology.base_iri, namespace=onto.get_namespace(onto.ontology.base_iri))
		pre = onto.get_namespace(base_iri='http://www.w3.org/ns/shacl#').PrefixDeclaration(prefix)
		pre.prefix = [prefix]
		pre.namespace = [onto.ontology.base_iri]
		o.declare.append(pre)

	@staticmethod
	def get_datatype_iris(type_name):
		"""
		get datatype iris
		Args:
			type_name: float/Floating point, int/Integer, string/String, bool/Boolean, long, anyURI, double
		Returns:

		"""
		if type_name in ['float', 'Floating point']:
			return IRIS['http://www.w3.org/2001/XMLSchema#float']
		elif type_name in ['int', 'Integer']:
			return IRIS['http://www.w3.org/2001/XMLSchema#integer']
		elif type_name in ['bool', 'Boolean']:
			return IRIS['http://www.w3.org/2001/XMLSchema#boolean']
		elif type_name.lower() == 'long':
			return IRIS["http://www.w3.org/2001/XMLSchema#long"]
		elif type_name.lower() == 'double':
			return IRIS["http://www.w3.org/2001/XMLSchema#double"]
		elif type_name in ['anyURI', 'anyuri', 'uri']:
			return IRIS["http://www.w3.org/2001/XMLSchema#anyURI"]
		else:
			return IRIS['http://www.w3.org/2001/XMLSchema#string']

	@staticmethod
	def handle_choices(option, option_name, choices, clazz, onto):
		"""
		handle available choices
		Args:
			option: tool option instance
			option_name: tool option name
			choices: list of available choices
			clazz: available choice class

		Returns:
			option
		"""
		choices_list = []
		for choice in choices:
			choiceValue = choice['choice'].strip()
			des = ' '.join(choice['description'])
			name = Preprocessor.replace_2_underline('[ ._]+', option_name + ' ' + choiceValue)
			# availableChoice = clazz(name, comment=locstr(option_name + ' available choice', lang='en'))
			availableChoice = clazz(0, prefLabel=locstr(name, lang='en'), comment=locstr(option_name + ' available choice', lang='en'))
			availableChoice.hasValue.append(choiceValue)
			if des.strip() != '-':
				availableChoice.description.append(des.strip())
				availableChoice.identifier = name.strip()
			option.availableChoice.append(availableChoice)
			choices_list.append(availableChoice)
		onto, rdf_list = OWLUtils.resources_2_rdf_list(onto, choices_list, False)
		# print(rdf_list)
		option.availableList.append(rdf_list)
		return option, onto


	@staticmethod
	def resources_2_rdf_list(onto, availables, isLiteral=True):
		_rdf = get_ontology('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
		_rdfs = get_ontology('http://www.w3.org/2000/01/rdf-schema#')
		with onto:
			class Resource(Thing):
				namespace = _rdfs
				isDefinedBy = 'http://www.w3.org/2000/01/rdf-schema#'
				label = "Resource"
				comment = "The class resource, everything."

			class Literal(Resource):
				namespace = _rdfs
				isDefinedBy = 'http://www.w3.org/2000/01/rdf-schema#'
				label = "Literal"
				comment = "The class of literal values, eg. textual strings and integers."

			class List(Resource):
				isDefinedBy = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
				namespace = _rdf
				label = "List"
				comment = "The class of RDF Lists."

			class first(ObjectProperty):
				isDefinedBy = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
				namespace = _rdf
				label = "first"
				comment = "The first item in the subject RDF list."
				domain = [List]
				range = [Resource]

			class rest(ObjectProperty):
				isDefinedBy = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
				namespace = _rdf
				label = "rest"
				comment = "The rest of the subject RDF list after the first item."
				domain = [List]
				range = [List]

		nil = List('nil', label='nil',
		           comment='The empty list, with no items in it. If the rest of a list is nil then the list has no more items in it.',
		           namespace=onto)

		def create_list(rdf_list, _resources):
			if isLiteral:
				rdf_list.first.append(Literal(_resources[0], namespace=onto, hasValue=[_resources[0]]))
			else:
				if onto[_resources[0]] is None:
					pass
				else:
					rdf_list.first.append(onto[_resources[0]])
			if len(_resources) == 1:
				rdf_list.rest.append(nil)
				return rdf_list
			_rdf_list = List(0, namespace=onto)
			rdf_list.rest.append(create_list(_rdf_list, _resources[1:]))
			return rdf_list

		_list = List(0, namespace=onto)
		create_list(_list, availables)
		return onto, _list

	@staticmethod
	def get_by_label(ont, obj_label):
		return ont.search_one(label=obj_label)

	@staticmethod
	def to_keywords(text):
		"""
		从工具或任务的名称、描述中提取关键词
		Returns:

		"""
		if len(text) == 0: return []
		# 设置 words 参数之后有可能报错
		words = keywords(text, split=True, deacc=True)
		if len(words) > 4:
			return words[:4]
		else:
			words = [word for word in words if len(word) > 1]
			return words

	@staticmethod
	def link_to_domain_concept(target_tool, tool_keywords):
		if tool_keywords is None:  # or len(tool_keywords) < 2:
			return
		if type(tool_keywords) is not list:
			tool_keywords = [tool_keywords]
		tool_keywords = [word for word in tool_keywords if word not in stopwords.words('english')]
		for keyword in tool_keywords:
			keyword = keyword.strip()
			if keyword == '': continue
			# too short, meaningless
			if len(keyword) < 2: continue
			keyword = keyword.lower()
			keyword = re.sub('(input|output|or)', '', keyword)
			keyword = re.sub('[()*]+', '', keyword)
			target_tool.subject.append(keyword)
			keyword = keyword.strip()
			if keyword == '': continue
			# it's weird that these words will cause stack overflow
			if keyword in ['viewshed', 'visibility', 'tangential curvature']:
				continue
			# print("keyword: " + keyword)
			concept = OWLUtils.search_domain_concept(keyword)
			# print(concept)
			if concept is None: continue
			if inspect.isclass(concept):
				continue
			if re.match("[a-zA-Z]+(input|output|option)[0-9]+", concept.name) is None:
				target_tool.domainConcept.append(concept)
		return target_tool

	@staticmethod
	def application_category(tool, broads, primaries, secondaries):
		"""
		adding applicaiton categories to tool

		Args:
			tool: geoprocessing tool
			broads:  broad applicaiton category
			primaries:primary applicaiton category concept words
			secondaries:  secondary applicaiton category concept words

		Returns:
			tool and geospatial
		"""
		if type(broads) is not list:
			broads = [broads]
		if type(secondaries) is not list:
			secondaries = [secondaries]
		if type(primaries) is not list:
			primaries = [primaries]

		for broad in broads:
			broad_concept = OWLUtils.search_domain_concept(broad)
			if broad_concept is not None:
				tool.domainConcept.append(broad_concept)
			tool.broadApplicationCategory.append(broad)
		for primary in primaries:
			primary_concept = OWLUtils.search_domain_concept(primary.lower())
			if primary_concept is not None:
				tool.domainConcept.append(primary_concept)
			tool.primaryApplicationCategory.append(primary)
		for secondary in secondaries:
			secondary_concept = OWLUtils.search_domain_concept(secondary)
			if secondary_concept is not None:
				tool.domainConcept.append(secondary_concept)
			tool.secondaryApplicationCategory.append(secondary)
		return tool

	@staticmethod
	def search_domain_concept(keyword):
		skos = get_ontology('/skos.rdf').load(only_local=True)
		dcterms = get_ontology('/dcterms.rdf').load(only_local=True)
		props = get_ontology('/UniProps.owl').load(only_local=True)
		geospatial = OWLUtils.load_geospatial()
		gcmd = get_ontology('/gcmd_keywords.owl').load(only_local=True)
		concept = gcmd.search_one(prefLabel=locstr(keyword, "en"))
		if concept is None:
			concept = geospatial.search_one(prefLabel=locstr(keyword, "en"))
		return concept

	@staticmethod
	def task_domain_concept(task, tool):
		"""add tool's linked concepts to linked atomic task"""
		concepts = tool.domainConcept
		for concept in concepts:
			task.domainConcept.append(concept)
		return task
