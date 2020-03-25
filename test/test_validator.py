#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/10 18:58
from validator import GeoValidator
import codecs
from rdflib import Namespace, Graph, RDFS, RDF
from pyshacl import rdfutil, Validator, validate
from datagraph import DataGraph

validator = GeoValidator()

l6_clip_point = '../data_graphs/L6_clip_point.ttl'
l6_input_polygon = '../data_graphs/L6_input_polygon.ttl'
l6_data_all = '../data_graphs/L6_all.ttl'
l6_shape = '../shapes/L6_SparqlShape.ttl'
qudt = '../ont/QUDT ALL UNITS.ttl'
data = '../ont/data.owl'
geo_file = '../ont/geosparql_vocab_all.rdf'
sf_file = '../ont/sf.rdf'

geo = rdfutil.load_from_source(geo_file)
ont = validator.read_graphs(geo_file, data, sf_file)
arcgis = Namespace("http://www.egc.org/ont/process/arcgis#")
data_ns = Namespace("http://www.egc.org/ont/data#")
process = Namespace("http://www.egc.org/ont/process#")


# g_geo = validator.read_graph(geo)
# v_shape = validator.read_graph(v_shape_file)

def test_case1():
	# d_graph = validator.read_graphs(l6_clip_point, l6_input_polygon)
	d_graph_all = rdfutil.load_from_source(l6_data_all)
	g_shape = rdfutil.load_from_source(l6_shape)
	# conforms, results_graph, results_text = validator.advanced_validate(d_graph, g_shape)
	conforms, results_graph, results_text = validator.validate_data(d_graph_all, g_shape, ont)
	# print(results_graph.serialize(format='turtle').decode('utf-8'))
	dg = DataGraph()
	dg.graph_2_file(results_graph, 'case1_report.ttl')
	# with codecs.open('case1_report.txt', 'w', 'utf-8') as f:
	# 	f.write(str(results_text))
	print('DONE')


L8_rule_file = '../shapes/L8_SPARQLRule.ttl'
dg = DataGraph()
rule = rdfutil.load_from_source(L8_rule_file)
dg_basin = rdfutil.load_from_source(l6_input_polygon)


def test_infer():
	"""
	the condition data:VectorDataShape is not satisfied since we have not provide the data.owl,
	thus no triples have been inferred
	"""
	conforms, expanded_graph = validator.infer_with_extended_graph(dg_basin, rule)
	# print(expanded_graph.serialize(format='turtle').decode('utf-8'))
	print(conforms)  # false,
	expanded_graph.bind('arcgis', arcgis)
	expanded_graph.bind('data', data_ns)
	expanded_graph.bind('process', process)

	# print(dg.graph_2_string(expanded_graph))
	# the same as the data graph
	dg.graph_2_file(expanded_graph, 'case2_graph_no_inferred.ttl')


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
	inferred.bind('arcgis', arcgis)
	inferred.bind('data', data_ns)
	inferred.bind('process', process)
	# extract the inferred triples from the mixed ontology graph
	inferred += expanded_graph.triples((None, process['from'], None))
	inferred += expanded_graph.triples((data_ns.in_features_data, process.isInputDataOf, None))
	# inferred += expanded_graph.triples((data_ns.in_features_data, RDF.type, None))
	# print(dg.graph_2_string(inferred))
	dg.graph_2_file(inferred, 'case2_graph.ttl')
