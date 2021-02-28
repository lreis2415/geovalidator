#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 16:10

from rdflib import BNode, Graph, RDF, Namespace, Literal
from rdflib.namespace import DCTERMS

g = Graph()
# namespaces
data = Namespace("http://www.egc.org/ont/data#")
saga = Namespace("http://www.egc.org/ont/process/saga#")
sh = Namespace("http://www.w3.org/ns/shacl#")
process = Namespace('http://www.egc.org/ont/gis/process#')
# prefixes
g.bind('data', data)
g.bind('sh', sh)
g.bind('saga', saga)
g.bind('process', process)
g.bind('dcterms', DCTERMS)

# SHACL shape graph
ds = saga.FlowAccumulationTopDownShape
g.add((ds, RDF.type, sh.NodeShape))
# [tool]_[parameter]
g.add((ds, sh.targetNode, saga.method_of_flow_accumulation_top_down))

p1 = BNode()
g.add((p1, sh.path, process.hasData))
g.add((p1, sh.minCount, Literal(0)))
g.add((p1, sh.maxCount, Literal(1)))
g.add((p1, sh.message, Literal('Must has at most one input value for option ‘Method’ of tool ‘Flow Accumulation (Top-Down)’', lang='en')))

g.add((ds, sh.property, p1))

# save as turtle file
g.serialize('../shapes/L2_FunctionalityLevelShape.ttl', format='turtle')
