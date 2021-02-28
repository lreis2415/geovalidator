#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/5 17:56
# https://github.com/RDFLib/pySHACL


from rdflib import Graph
from rdflib.util import guess_format
from pyshacl import validate, Validator
from datagraph import DataGraph
from utils import Utils


class GeoValidator(object):

	@staticmethod
	def read_graphs(*ont_graphs):
		"""
		read and merge a set of ont graphs
		:param ont_graphs:
		:return: A merge of a set of RDF graphs
		"""
		g = Graph()
		for ont in ont_graphs:
			f = guess_format(ont)
			g.parse(ont, format=f)
		return g

	@staticmethod
	def data_2_graph(parameter_id:str, data, data_theme=None, data_type=None):
		"""
		read input data and generate RDF graph
		:param parameter_id: parameter identifier, indicates which parameter this data is prepared for
		:param data: input data path or value
		:param data_theme: data theme. e.g., DEM, soil, landuse, city, etc.
		:param data_type: automatically detect if is None. 0 for raster data; 1 for vector data; 2 for general (non-geospatial) data
		:return: data graph
		"""
		_dg = DataGraph()
		if data_type is None:
			data_type = Utils.detect_data_type(data)
		# raster data
		if data_type == 0:
			graph = _dg.raster_graph(parameter_id, data, data_theme)
		# vector data
		elif data_type == 1:
			graph = _dg.vector_graph(parameter_id, data, data_theme)
		# non-geospatial data
		else:
			graph = _dg.general_graph(parameter_id, data, data_theme)
		return graph

	@staticmethod
	def validate_data(data_graph, shape_graph, ont=None):
		"""
		validate_data input data against a predefined shape graph
		:param data_graph:
		:param shape_graph:
		:param ont:
		:return:
		"""
		results = validate(data_graph, shacl_graph=shape_graph,
		                   ont_graph=ont, inference='rdfs', debug=False)
		# conforms, results_graph, results_text = results
		return results

	@staticmethod
	def advanced_validate(data_graph, shape_graph, ont=None):
		# enable SHACL advanced features: rules, custom targets
		results = validate(data_graph, shacl_graph=shape_graph, ont_graph=ont,
		                   advanced=True, inference='rdfs', debug=False)
		# conforms, results_graph, results_text = results
		# the results_graph just contains the validation report, not inferred triples
		return results

	@staticmethod
	def infer_with_extended_graph(data_graph, shacl_rule, ont=None):
		"""
		use validate directly cannot get the inferred triples
		:param data_graph:
		:param shacl_rule:
		:param ont:
		:return:
		"""
		v = Validator(data_graph=data_graph, shacl_graph=shacl_rule,
		              options={"inference": "rdfs", "advanced": True}, ont_graph=ont)
		conforms, report_graph, report_text = v.run()
		# mixed in the extra-ontology graph
		expanded_graph = v.target_graph
		return conforms, expanded_graph
