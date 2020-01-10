#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 15:47

from rdflib import BNode, Graph, RDF, Namespace, Literal, XSD

g = Graph()
# namespaces
data = Namespace("http://www.egc.org/ont/data#")
saga = Namespace("http://www.egc.org/ont/process/saga#")
sh = Namespace("http://www.w3.org/ns/shacl#")
geo = Namespace('http://www.opengis.net/ont/geosparql#')
sf = Namespace('http://www.opengis.net/ont/sf#')
# prefixes
g.bind('data', data)
g.bind('sh', sh)
g.bind('saga', saga)
g.bind('geo', geo)
g.bind('sf', sf)
# SHACL shape graph
sl = saga.para_significance_level
g.add((sl, RDF.type, sh.NodeShape))
g.add((sl, RDF.type, saga.SagaOption))
g.add((sl, sh.minCount, Literal(1)))
g.add((sl, sh.maxCount, Literal(1)))
g.add((sl, sh.targetNode, saga.para_significance_level_data))
# property
p1 = BNode()
g.add((p1, sh.path, data.dataContent))
g.add((p1, sh.datatype, XSD.float))
g.add((p1, sh.defaultValue, Literal(5.0, datatype=XSD.float)))
g.add((p1, sh.minCount, Literal(1)))
g.add((p1, sh.maxCount, Literal(1)))
g.add((p1, sh.minInclusive, Literal(0, datatype=XSD.float)))
g.add((p1, sh.maxInclusive, Literal(100.0, datatype=XSD.float)))
g.add((p1, sh.description, Literal('Significance level (aka p-value) as threshold for automated predictor selection, given as percentage', lang='en')))
g.add((p1, sh.message, Literal('The acceptable value range for significance level is 0 to 100.0', lang='en')))
g.add((p1, sh.message, Literal('参数significance level的取值范围为0 到 100.0', lang='zh-cn')))
g.add((sl, sh.property, p1))

# save as turtle file
g.serialize('../shapes/L4_SagaSignLevelShape.ttl', format='turtle')
