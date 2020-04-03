#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/10/28 11:41
import re
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import DC, OWL, SKOS, RDF, RDFS
from JSON2OWL.OwlConvert.Preprocessor import Preprocessor

graph = Graph()
graph.load('../OwlConvert/shacl.rdf')
graph.bind('skos', URIRef('http://www.w3.org/2004/02/skos/core#'))
graph.bind('data', URIRef('http://www.egc.org/ont/data#'))
graph.bind('datasource', URIRef('http://www.egc.org/ont/datasource#'))
graph.bind('cyber', URIRef('http://www.egc.org/ont/gis/cyber#'))
graph.bind('props', URIRef('http://www.egc.org/ont/base/props#'))
graph.bind('context', URIRef('http://www.egc.org/ont/context#'))
graph.bind('saga', URIRef('http://www.egc.org/ont/process/saga#'))
graph.bind('dcterms', URIRef('http://purl.org/dc/terms/'))
graph.bind('task', URIRef('http://www.egc.org/ont/context/task#'))
graph.bind('sh', URIRef('http://www.w3.org/ns/shacl#'))
graph.bind('process', URIRef('http://www.egc.org/ont/gis/process#'))
graph.bind('dc', URIRef('http://purl.org/dc/elements/1.1/'))
graph.bind('owl', URIRef('http://www.w3.org/2002/07/owl#'))
graph.bind('swrl', URIRef('http://www.w3.org/2003/11/swrl#'))

saga_uri = "http://www.egc.org/ont/process/saga#"
saga = Namespace(saga_uri)
sh = Namespace('http://www.w3.org/ns/shacl#')
import os
import json


def gen_shacl(json_data):
	for d in json_data:
		name = Preprocessor.toolname_underline(d['name'])
		name = re.sub("[()-*,/]_", " ", name).strip()
		if d['parameters']:
			for item, itemValue in d['parameters'].items():
				if item == 'options':
					for optionItem in itemValue:
						shape = URIRef(saga_uri + name.replace(" ", '') + 'Shape')
						graph.add((shape, RDF.type, sh.ShapeNode))
						graph.add((shape, sh.TargetNode, URIRef(saga_uri + name)))
						shapeGraph = BNode()


if __name__ == "__main__":
	module_path = os.path.dirname(__file__)
	with open(module_path + '/saga.json', 'r') as f:
		jdata = json.load(f)  # list
