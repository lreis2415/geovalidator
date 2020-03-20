#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/10 18:58
from validator import GeoValidator
import codecs
from pyshacl import rdfutil
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
	dg.graph_2_file(results_graph,'case1_report.ttl')
	# with codecs.open('case1_report.txt', 'w', 'utf-8') as f:
	# 	f.write(str(results_text))
	print('DONE')


L8_rule_file = '../shapes/L8_SPARQLRule.ttl'

# 如何获得推理之后的三元组？
def test_rule():
	rule = rdfutil.load_from_source(L8_rule_file)
	dg_basin = rdfutil.load_from_source(l6_input_polygon)

	# r = validator.advanced_validate(dg_basin, rule, ont)
	r = validator.advanced_validate(dg_basin, rule)
	conforms, results_graph, results_text = r
	# print(results_text)
	print(results_graph.serialize(format='turtle').decode('utf-8'))
