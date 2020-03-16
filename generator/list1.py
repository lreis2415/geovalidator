#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 15:47

from rdflib import BNode, Graph, RDF, Namespace, Literal

g = Graph()
# namespaces
data = Namespace("http://www.egc.org/ont/data#")
sh = Namespace("http://www.w3.org/ns/shacl#")
# prefixes
g.bind('data', data)
g.bind('sh', sh)
# SHACL shape graph
vs = data.VectorShape
g.add((vs, RDF.type, sh.NodeShape))
g.add((vs, sh.targetClass, data.VectorData))
g.add((vs, sh.description, Literal('All instances of data:VectorData will be checked', lang='en')))

# save as turtle file
g.serialize('../shapes/L1_VectorDataShape.ttl', format='turtle')
