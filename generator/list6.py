#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 15:47

from rdflib import BNode, Graph, RDF, Namespace, Literal,XSD

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
vs = data.VectorDataEPSGShape
g.add((vs, RDF.type, sh.NodeShape))
g.add((vs, sh.node, data.VectorDataShape))
p = BNode()
g.add((p, sh.path, data.hasEPSG))
g.add((p, sh.minCount, Literal(1)))
g.add((p, sh.maxCount, Literal(1)))
g.add((p, sh.node,data.VectorDataShape))
g.add((vs, sh.property, p))

# SHACL shape graph
inf = arcgis.para_in_features
g.add((inf, RDF.type, sh.NodeShape))
g.add((inf, RDF.type, arcgis.ArcGISInput))
g.add((inf, sh.targetNode, arcgis.para_in_features_data))
g.add((inf, sh.minCount, Literal(1)))
g.add((inf, sh.maxCount, Literal(1)))
g.add((inf, sh.description, Literal('Parameter in_features: the features to be clipped by ArcGIS Clip analysis',lang='en')))
g.add((inf, sh.node,data.VectorDataEPSGShape))

# property 1
p1 = BNode()
g.add((p1, sh.path, data.dataContent))
g.add((p1, sh.datatype, XSD.string))
g.add((p1, sh.minLength, Literal(4)))
g.add((p1, sh.minCount, Literal(1)))
g.add((p1, sh.maxCount, Literal(1)))
g.add((inf, sh.property, p1))

# save as turtle file
g.serialize('../shapes/L6_GeoDataShape.ttl', format='turtle')
