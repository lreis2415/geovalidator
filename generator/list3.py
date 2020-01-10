#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 19:14

from rdflib import BNode, Graph, RDF, Namespace, Literal, RDFS

g = Graph()
# namespaces
data = Namespace("http://www.egc.org/ont/data#")
sh = Namespace("http://www.w3.org/ns/shacl#")
geo = Namespace('http://www.opengis.net/ont/geosparql#')
sf = Namespace('http://www.opengis.net/ont/sf#')
task = Namespace('http://www.egc.org/ont/context/task#')
dta = Namespace('http://www.egc.org/ont/domain/dta#')

# prefixes
g.bind('data', data)
g.bind('sh', sh)
g.bind('geo', geo)
g.bind('sf', sf)
g.bind('task', task)
g.bind('dta', dta)
# SHACL shape graph
hctask = task.HydroParamSpatialPatternCalcTask
g.add((hctask, RDF.type, sh.NodeShape))
g.add((hctask, RDF.type, RDFS['Class']))
g.add((hctask, sh.description, Literal('A class that includes instances such as flow accumulation and topographic index', lang='en')))
p = BNode()
g.add((hctask, sh.property, p))
g.add((p, sh.path, task.processAlgorithm))
g.add((p, sh.nodeKind, sh.IRI))
g.add((p, sh.severity, sh.Warning))
g.add((p, sh.message, Literal('Calculation of spatial patterns of hydrologic parameters should use Multiple Flow Direction (MFD) algorithms', lang='en')))
g.add((p, sh['class'], dta.MFDAlgorithm))

g.serialize('../shapes/L3_FlowDirectionAlgShape', format='turtle')
