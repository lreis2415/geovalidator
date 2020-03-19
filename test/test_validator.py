#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/10 18:58
from validator import GeoValidator
import codecs
from pyshacl import rdfutil

validator = GeoValidator()

l6_clip_point = '../data_graphs/L6_clip_point.ttl'
l6_input_polygon = '../data_graphs/L6_input_polygon.ttl'
l6_data_all = '../data_graphs/L6_all.ttl'
l6_shape = '../shapes/L6_SparqlShape.ttl'
v_shape_file = '../shapes/L5_VectorDataShape.ttl'
qudt = '../ont/QUDT ALL UNITS.ttl'
geo_file = '../ont/geosparql_vocab_all.rdf'

geo = rdfutil.load_from_source(geo_file)
vector_shape = rdfutil.load_from_source(v_shape_file)


# g_geo = validator.read_graph(geo)
# v_shape = validator.read_graph(v_shape_file)


def test_case1():
	# d_graph = validator.read_graphs(l6_clip_point, l6_input_polygon)
	d_graph_all = rdfutil.load_from_source(l6_data_all)
	g_shape = rdfutil.load_from_source(l6_shape)
	# conforms, results_graph, results_text = validator.advanced_validate(d_graph, g_shape)
	conforms, results_graph, results_text = validator.advanced_validate(d_graph_all, g_shape)
	with codecs.open('case1_report.txt', 'w', 'utf-8') as f:
		f.write(str(results_text))
	print('DONE')
