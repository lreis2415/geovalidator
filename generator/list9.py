#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 15:47

from rdflib import BNode, Graph, RDF, Namespace, Literal, XSD
from rdflib.collection import Collection

g = Graph()
# namespaces
data = Namespace("http://www.egc.org/ont/data#")
process = Namespace("http://www.egc.org/ont/process#")
soft = Namespace("http://www.egc.org/ont/cyber#")
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
g.bind('soft', soft)
# part 1: a standard shape graph
crs = data.CRSExistenceShape
g.add((crs, RDF.type, sh.NodeShape))
p = BNode()
g.add((p, sh.path, data.hasCRS))
g.add((p, sh.minCount, Literal(1)))
g.add((p, sh.maxCount, Literal(1)))
g.add((p, sh.datatype, XSD.string))
g.add((p, sh.minLength, Literal(3)))
g.add((p, sh.description, Literal('Checks whether a data set has a CRS.', lang='en')))
g.add((crs, sh.property, p))

# part 2: a SHACL triple rule
rrs = data.ReprojectRuleShape
g.add((rrs, RDF.type, sh.NodeShape))
g.add((rrs, sh.targetClass, arcgis.ArcGISTool))

rule = BNode()
g.add((rule, RDF.type, sh.TripleRule))
g.add((rule, sh.subject, sh.this))
g.add((rule, sh.predicate, process.preprocessor))
g.add((rule, sh.object, arcgis.project_raster))
condition = BNode()
cp = BNode()
g.add((cp, sh.path, soft.inputData))

l = BNode()
b_not = BNode()
b_node = BNode()
g.add((b_node, sh.node, data.CRSExistenceShape))
g.add((b_not, sh['not'], b_node))
b_value = BNode()
g.add((b_value, sh.path, RDF.type))
g.add((b_value, sh.hasValue, data.RasterData))

Collection(g, l, [b_not, b_value])
g.add((cp, sh['and'], l))

g.add((condition, sh.property, cp))
g.add((rule, sh.condition, condition))

g.add((rrs, sh.rule, rule))

# save as turtle file
g.serialize('../shapes/L9_TripleRule.ttl', format='turtle')
