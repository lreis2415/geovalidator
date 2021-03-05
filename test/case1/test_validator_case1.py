#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/10 18:58
from validator import GeoValidator
from rdflib import Namespace, Graph
from pyshacl import rdfutil
from datagraph import DataGraph
from utils import DATA, GEO, ArcGIS, PROCESS
import pytest

validator = GeoValidator()


# ontologies
qudt = '../../ont/QUDT ALL UNITS.ttl'
data = '../../ont/data.owl'
dcat = '../../ont/dcat2.ttl'
geo_file = '../../ont/geosparql_vocab_all.rdf'
sf_file = '../../ont/sf.rdf'

geo = rdfutil.load_from_source(geo_file)
ont = validator.read_graphs(geo_file, data, sf_file, dcat, qudt)

case_data = './case1_data_graphs.ttl'
case_shape = './case1_shapes_m.ttl'


def test_case1():
	# d_graph = validator.read_graphs(l6_clip_point, l6_input_polygon)
	d_graph = rdfutil.load_from_source(case_data)
	g_shape = rdfutil.load_from_source(case_shape)
	# conforms, results_graph, results_text = validator.advanced_validate(d_graph, g_shape)
	conforms, results_graph, results_text = validator.validate_data(d_graph, g_shape, ont)
	# print(results_graph.serialize(format='turtle').decode('utf-8'))
	dg.graph_2_file(results_graph, 'case1_report.ttl')
	# with codecs.open('case1_report.txt', 'w', 'utf-8') as f:
	# 	f.write(str(results_text))
	print('DONE')


# L8_rule_file = '../../shapes/L8_SPARQLRule.ttl'
dg = DataGraph()
# rule = rdfutil.load_from_source(L8_rule_file)
# dg_basin = rdfutil.load_from_source(l6_input_polygon)


# def test_infer():
# 	"""
# 	the condition data:VectorDataShape is not satisfied since we have not provide the data.owl,
# 	thus no triples have been inferred
# 	"""
# 	conforms, expanded_graph = validator.infer_with_extended_graph(dg_basin, rule)
# 	# print(expanded_graph.serialize(format='turtle').decode('utf-8'))
# 	print(conforms)  # false,
# 	expanded_graph.bind('arcgis', ArcGIS)
# 	expanded_graph.bind('data', DATA)
# 	expanded_graph.bind('process', PROCESS)
#
# 	# print(dg.graph_2_string(expanded_graph))
# 	# the same as the data graph
# 	dg.graph_2_file(expanded_graph, 'case2_graph_no_inferred.ttl')


def test_infer_ont():
	"""
	if we use TopQuadrant's shaclinfer.bat, we can get the inferred triples directly
	if we provide a extra ontology
	:return:
	"""
	# inferred graph mixed with ont
	conforms, expanded_graph = validator.infer_with_extended_graph(dg_basin, rule, ont)
	# print(expanded_graph.serialize(format='turtle').decode('utf-8'))

	inferred = Graph()
	inferred.bind('arcgis', ArcGIS)
	inferred.bind('data', DATA)
	inferred.bind('process', PROCESS)
	# extract the inferred triples from the mixed ontology graph
	inferred += expanded_graph.triples((None, PROCESS['from'], None))
	inferred += expanded_graph.triples((DATA.in_features_data, PROCESS.isInputDataOf, None))
	# inferred += expanded_graph.triples((data_ns.in_features_data, RDF.type, None))
	# print(dg.graph_2_string(inferred))
	dg.graph_2_file(inferred, 'case2_graph.ttl')


def test_data_on_the_fly_case1():
	points = '../data/Heihe_Meteorology_Station_Distribution.shp'
	basin = '../data/Heihe_Basin_Boundary_2010.shp'
	# read raw input data and translate into data graphs
	clip_point = dg.vector_graph('clip_features', points, 'Meteorology_Station')
	in_polygon = dg.vector_graph('in_features', basin, 'Basin')
	# functionality-level data graph
	func_graph = dg.functionality_data_graph(ArcGIS.clip_analysis, clip_point, in_polygon)
	# all
	data_graph = func_graph + clip_point + in_polygon
	dg.graph_2_file(data_graph,'all.ttl')
	# validate input data against shapes graphs
	g_shape = rdfutil.load_from_source(l6_shape)
	conforms, results_graph, results_text = validator.validate_data(data_graph, g_shape, ont)
	dg.graph_2_file(results_graph, 'case1_report_2.ttl')

if __name__ =="__main__":
	pytest.main('[test_validator_case1::test_case1]')