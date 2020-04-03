#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/11/8 15:01

from owlready2 import *
import json
import re
from rdflib import BNode, RDF, Graph, URIRef, Namespace,Literal
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils
from JSON2OWL.OwlConvert.Preprocessor import Preprocessor

#
# module_uri = 'http://www.egc.org/ont/process/saga'
# onto = get_ontology(module_uri)
# # onto, skos, dcterms, props = OWLUtils.load_common(onto)
# onto, sh, skos, dcterms, props, foaf = OWLUtils.load_common(onto)
# onto, geospatial = OWLUtils.load_geo_vocabl(onto)
# onto, gb, task, data, cyber, context = OWLUtils.load_common_for_process_tool(onto)
# print('ontologies imported')
#
# sh_ns = onto.get_namespace(sh.base_iri)
# data_ns = onto.get_namespace(data.base_iri)
# cyber_ns = onto.get_namespace(cyber.base_iri)
# print(cyber_ns.supportsDataFormat)
# with onto:
# 	class SagaTool(gb.GeoprocessingFunctionality):
# 		pass
# a = SagaTool('a')
#
# a.property.append(pshape)

g = Graph()
# g.parse()
g.load('../OwlConvert/data.owl')
g.load('../OwlConvert/shacl.rdf')
g.load('../OwlConvert/skos.rdf')
Data = Namespace('http://www.egc.org/ont/data#')
Cyber = Namespace('http://www.egc.org/ont/gis/cyber#')
Skos = Namespace('http://www.w3.org/2004/02/skos/core#')
Sh = Namespace('http://www.w3.org/ns/shacl#')
pshape = BNode()
g.add((pshape, RDF.type, Sh.PropertyShape))
g.add((pshape,Sh.path, Data.dataContent))
g.add((pshape,Sh.minCount, Literal(1)))

