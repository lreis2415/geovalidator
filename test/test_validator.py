#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/10 18:58
from validator import GeoValidator
from rdflib import Graph
from pyshacl import validate

validator = GeoValidator()

l7_clip_line = '../data_graphs/L7_clip_line.ttl'
l7_input_polygon = '../data_graphs/L7_input_polygon.ttl'
l7_shape = '../shapes/L7_SparqlShape.ttl'
v_shape_file = '../shapes/L1_VectorDataShape.ttl'
qudt = '../ont/QUDT ALL UNITS.ttl'
geo = '../ont/geosparql_vocab_all.rdf'

g_geo = validator.read_graph(geo)
v_shape = validator.read_graph(v_shape_file)


def test_clip():
	g_in = validator.read_graph(l7_input_polygon)
	g_clip = validator.read_graph(l7_clip_line)
	conforms, results_graph, results_text = validator.validate_data(g_in, l7_shape, g_geo)
	print(conforms)


def test_case1():
	d_graph = validator.read_graphs(l7_clip_line, l7_input_polygon)
	# d_graph = validator.read_graph('../data_graphs/L7_all.ttl')
	g_shape = validator.read_graph(l7_shape)
	conforms, results_graph, results_text = validator.advanced_validate(d_graph, g_shape)
	print(results_text)


def test_pyshacl():
	results = validate('../data_graphs/L7_all.ttl', shacl_graph='../shapes/L7_SparqlShape.ttl', inference='rdfs', debug=True)
	print(results)
