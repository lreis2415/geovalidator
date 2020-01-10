#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 15:47

from rdflib import BNode, Graph, RDF, Namespace, Literal

g = Graph()
# namespaces
data = Namespace("http://www.egc.org/ont/data#")
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
# SHACL shape graph
vs = data.VectorShape
g.add((vs, RDF.type, sh.NodeShape))
g.add((vs, sh.targetClass, data.VectorData))
g.add((vs, sh.description, Literal('All instances of data:VectorData will be checked', lang='en')))
# property 1
p1 = BNode()
g.add((p1, sh.path, data.dataFormat))
g.add((p1, sh['class'], data.VectorFormat))
g.add((p1, sh.defaultValue, data.ESRI_Shapefile))
g.add((p1, sh.minCount, Literal(1)))
g.add((p1, sh.maxCount, Literal(1)))
g.add((p1, sh.message, Literal('Input data should declare a data format information, and it must be an instance of class data:VectorFormat ', lang='en')))
g.add((vs, sh.property, p1))
# property 2
p2 = BNode()
g.add((p2, sh.path, geo.hasGeometry))
g.add((p2, sh['class'], sf.Geometry))
g.add((p2, sh.minCount, Literal(1)))
g.add((p2, sh.maxCount, Literal(1)))
g.add((p2, sh.message, Literal('Vector input data must declare a geometry type', lang='en')))
g.add((vs, sh.property, p2))
# save as turtle file
g.serialize('../shapes/L1_VectorDataShape.ttl', format='turtle')
