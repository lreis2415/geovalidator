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
g.add((ds, sh.targetNode, saga.flow_accumulation_top_down))

p1 = BNode()
g.add((p1, sh.path, process.hasInputData))

qs = BNode()
g.add((qs, sh.path, DCTERMS.identifier))
g.add((qs, sh.hasValue, Literal('method')))
g.add((p1, sh.qualifiedValueShape, qs))

g.add((p1, sh.qualifiedValueShape, qs))
g.add((p1, sh.qualifiedMinCount, Literal(0)))
g.add((p1, sh.qualifiedMaxCount, Literal(1)))
g.add((p1, sh.qualifiedValueShapesDisjoint, Literal(True)))
g.add((p1, sh.message, Literal('Must have exactly one input value with identifier ‘method’ '
                               'for option ‘Method’ of tool ‘Flow Accumulation (Top-Down)’', lang='en')))

g.add((ds, sh.property, p1))

# save as turtle file
g.serialize('../shapes/L2_FunctionalityLevelShape.ttl', format='turtle')
