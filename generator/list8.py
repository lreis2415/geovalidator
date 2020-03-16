#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 15:47

from rdflib import BNode, Graph, RDF, Namespace, Literal
from utils import Utils

g = Graph()
# namespaces
data = Namespace("http://www.egc.org/ont/data#")
process = Namespace("http://www.egc.org/ont/process#")
arcgis = Namespace("http://www.egc.org/ont/process/arcgis#")
sh = Namespace("http://www.w3.org/ns/shacl#")
geo = Namespace('http://www.opengis.net/ont/geosparql#')
sf = Namespace('http://www.opengis.net/ont/sf#')
# prefixes
g.bind('data', data)
g.bind('sh', sh)
g.bind('arcgis', arcgis)
g.bind('geo', geo)
g.bind('sf', sf)
g.bind('process', process)

# a SHACL triple rule
rrs = data.ProjectVectorDataRule
g.add((rrs, RDF.type, sh.NodeShape))
g.add((rrs, sh.targetClass, arcgis.ArcGISTool))
g.add((rrs, sh.description,
       Literal('For all arcgis tools, if their vector input data do not have a CRS, the ‘project’ tool will be inferred as a pre-processing tool for the data.', lang='en')))

rule = BNode()
g.add((rule, RDF.type, sh.TripleRule))
g.add((rule, sh.subject, sh.this))
g.add((rule, sh.predicate, process.preprocessor))
g.add((rule, sh.object, arcgis.project))

# conditions
cn = BNode()
g.add((cn, sh.path, process.inputData))

# condition 1
b_value = BNode()
g.add((b_value, sh.path, RDF.type))
g.add((b_value, sh.hasValue, data.VectorData))
# condition 2
b_not = BNode()
b_node = BNode()
g.add((b_node, sh.node, data.CRSExistenceShape))
g.add((b_not, sh['not'], b_node))
g, c, l = Utils.values_collection(g, [b_not, b_value])
g.add((cn, sh['and'], l))

condition = BNode()
g.add((condition, sh.property, cn))
g.add((rule, sh.condition, condition))
g.add((rrs, sh.rule, rule))

# save as turtle file
g.serialize('../shapes/L8_TripleRule.ttl', format='turtle')
