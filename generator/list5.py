#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 15:47

from rdflib import Graph, RDF, Literal, BNode
from utils import DATA, SH, SF, GEO

g = Graph()
# EPSGShape
g.parse('../shapes/L4_CRSShape.ttl', format='turtle')

# prefixes
g.bind('data', DATA)
g.bind('sh', SH)
# SHACL shape graph
vds = DATA.VectorDataShape
g.add((vds, RDF.type, SH.NodeShape))
g.add((vds, SH.targetClass, DATA.VectorData))

geon = BNode()
g.add((geon, SH.path, GEO.hasGeometry))
g.add((geon, SH['class'], SF.Geometry))
g.add((geon, SH.minCount, Literal(1)))
g.add((geon, SH.maxCount, Literal(1)))
g.add((geon, SH.message, Literal('Vector data must declare a geometry type ', lang='en')))
g.add((vds, SH.property, geon))

epg = BNode()
g.add((epg, SH.path, DATA.hasEPSG))
g.add((epg, SH.minCount, Literal(1)))
g.add((epg, SH.maxCount, Literal(1)))
# need to import shape file
# e.g., <> owl:imports <http://example.org/UserShapes> .
g.add((epg, SH.node, DATA.EPSGShape))
g.add((vds, SH.property, epg))

format_n = BNode()
g.add((format_n, SH.path, DATA.dataFormat))
g.add((format_n, SH.minCount, Literal(1)))
g.add((format_n, SH.maxCount, Literal(1)))
g.add((format_n, SH['class'], DATA.VectorFormat))
g.add((format_n, SH.message, Literal('Must be vector data format')))
g.add((vds, SH.property, format_n))
# save as turtle file
g.serialize('../shapes/L5_VectorDataShape.ttl', format='turtle')
