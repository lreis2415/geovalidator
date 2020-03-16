#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 16:10

from rdflib import BNode, Graph, RDF, Namespace, Literal, XSD
from utils import Utils


g = Graph()
# namespaces
data = Namespace("http://www.egc.org/ont/data#")
saga = Namespace("http://www.egc.org/ont/process/saga#")
sh = Namespace("http://www.w3.org/ns/shacl#")
process = Namespace('http://www.egc.org/ont/gis/process#')
task = Namespace('http://www.egc.org/ont/context/task#')
# prefixes
g.bind('data', data)
g.bind('sh', sh)
g.bind('saga', saga)
g.bind('process', process)
g.bind('task', task)

# SHACL shape graph
ds = saga.option_method
g.add((ds, RDF.type, sh.NodeShape))
g.add((ds, RDF.type, saga.SagaOption))
g.add((ds, sh.targetNode, data.method_value))
g.add((ds, sh.description, Literal('Constraints for SAGA tool Flow Accumulation (Top-Down)', lang='en')))

p1 = BNode()
g.add((p1, sh.path, data.dataContent))
g.add((p1, sh.minCount, Literal(1)))
g.add((p1, sh.maxCount, Literal(1)))
g.add((p1, sh.defaultValue, Literal(4)))
g.add((p1, sh.minInclusive, Literal(0)))
g.add((p1, sh.maxInclusive, Literal(6)))
g.add((p1, sh.datatype, XSD.int))
g.add((p1, sh.message, Literal(' value of option "method" for selecting flow direction algorithm  ’', lang='en')))
g.add((ds, sh.property, p1))

# SHACL SPARQL
sparql_node = BNode()
g.add((sparql_node, sh.message, Literal(
	'Multiple flow direction (MFD) algorithms are better than single flow direction (SFD) algorithms when calculating the spatial pattern of hydrological parameters such as topo-graphic index.',
	lang='en')))
g, sparql_node = Utils.shacl_prefixes(g, sparql_node,
                                 [('process', process), ('task', task), ('data', data)])

# report a warning instead of violation
g.add((sparql_node, sh.severity, sh.Warning))
sparql_str ="""
SELECT  $this  ?value
WHERE {
	$this process:isOptionOf/process:usedByTask ?task. 
	$this data:dataContent ?value. 
	FILTER(IF((?task a task:HydroParamSpatialPatternCalc) && (3<?value),false,true))}
"""
g.add((ds, sh.select, Literal(sparql_str)))
g.add((ds, sh.sparql, sparql_node))

# save as turtle file
g.serialize('../shapes/L3_ParameterAndApplicationLevelShape.ttl', format='turtle')
