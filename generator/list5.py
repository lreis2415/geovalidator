#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 15:47

from rdflib import Graph, RDF, Namespace, Literal, BNode

g = Graph()
# namespaces
data = Namespace("http://www.egc.org/ont/data#")
sh = Namespace("http://www.w3.org/ns/shacl#")
geo = Namespace('http://www.opengis.net/ont/geosparql#')
sf = Namespace('http://www.opengis.net/ont/sf#')
# prefixes
g.bind('data', data)
g.bind('sh', sh)
# SHACL shape graph
vds = data.VectorDataShape
g.add((vds, RDF.type, sh.NodeShape))
g.add((vds, sh.targetClass, data.VectorData))
geon = BNode()
g.add((geon, sh.path, geo.hasGeometry))
g.add((geon, sh['class'], sf.Geometry))
g.add((geon, sh.minCount, Literal(1)))
g.add((geon, sh.maxCount, Literal(1)))
g.add((geon, sh.message, Literal('Vector data must declare a geometry type ', lang='en')))
g.add((vds, sh.property, geon))

epg = BNode()
g.add((epg, sh.path, data.hasEPSG))
g.add((epg, sh.minCount, Literal(1)))
g.add((epg, sh.maxCount, Literal(1)))
# need to import shape file
# e.g., <> owl:imports <http://example.org/UserShapes> .
g.add((epg, sh.node, data.EPSGShape))
g.add((vds, sh.property, epg))

format_n = BNode()
g.add((format_n, sh.path, data.dataFormat))
g.add((format_n, sh.minCount, Literal(1)))
g.add((format_n, sh.maxCount, Literal(1)))
g.add((format_n, sh['class'], data.VectorDataFormat))
g.add((vds, sh.property, format_n))
# save as turtle file
g.serialize('../shapes/L5_VectorDataShape.ttl', format='turtle')
