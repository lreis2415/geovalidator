#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 15:47

from rdflib import Graph, RDF, Literal
from utils import DATA, SH

g = Graph()

# prefixes
g.bind('data', DATA)
g.bind('sh', SH)
# SHACL shape graph
vs = DATA.VectorShape
g.add((vs, RDF.type, SH.NodeShape))
g.add((vs, SH.targetClass, DATA.VectorData))
g.add((vs, SH.description, Literal('All instances of data:VectorData will be checked', lang='en')))

# save as turtle file
g.serialize('../shapes/L1_VectorDataShape.ttl', format='turtle')
