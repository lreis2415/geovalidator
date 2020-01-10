#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 15:47

from rdflib import Graph, RDF, Namespace, Literal, XSD

g = Graph()
# namespaces
data = Namespace("http://www.egc.org/ont/data#")
sh = Namespace("http://www.w3.org/ns/shacl#")
# prefixes
g.bind('data', data)
g.bind('sh', sh)
# SHACL shape graph
es = data.EPSGShape
g.add((es, RDF.type, sh.NodeShape))
g.add((es, sh.targetObjectsOf, data.hasEPSG))
g.add((es, sh.message,
       Literal('Invalid EPSG code! Must matchs the pattern  ‘urn:ogc:def:crs:EPSG:[version]:[code]’,  ‘http://www.opengis.net/def/crs/EPSG/[version]/[code]’, or ‘EPSG:[code]’',
               lang='en')))
g.add((es, sh.datatype, XSD.string))
g.add((es, sh.minLength, Literal(9)))
g.add((es, sh.pattern, Literal('^(urn:ogc:def:crs:EPSG:[0-9.]{,7}:[0-9]{4,5})|^(http://www.opengis.net/def/crs/EPSG/[0-9.]{1,7}/[0-9]{4,5})|^(EPSG:[0-9]{4,5}')))
g.add((es, sh.flag, Literal('i')))
g.add((es, sh.message, Literal('Input data should declare a data format information, and it must be an instance of class data:VectorFormat ', lang='en')))

# save as turtle file
g.serialize('../shapes/L5_EPSGShape.ttl', format='turtle')
