#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 16:10

from rdflib import BNode, Graph, RDF, Namespace, Literal, XSD
from utils import Utils


g = Graph()
# namespaces
data = Namespace("http://www.egc.org/ont/data#")
arcgis = Namespace("http://www.egc.org/ont/process/arcgis#")
sh = Namespace("http://www.w3.org/ns/shacl#")
process = Namespace('http://www.egc.org/ont/process#')
task = Namespace('http://www.egc.org/ont/task#')
context = Namespace('http://www.egc.org/ont/context#')
# prefixes
g.bind('data', data)
g.bind('sh', sh)
g.bind('arcgis', arcgis)
g.bind('process', process)
g.bind('task', task)
g.bind('context', context)

# SHACL shape graph

# data shapes
isds = arcgis.inSurfaceRasterDataShape
g.add((isds, RDF.type, sh.NodeShape))
g.add((isds, sh.targetNode, arcgis.in_surface_raster))
g.add((isds, sh.description, Literal('Constraints for ArcGIS tool Flow Direction input data', lang='en')))

p_theme = BNode()
# TODO how to add shacl paths?  (dcterms:subject rdf:label)
g.add((p_theme, sh.path, data.hasData))
g.add((p_theme, sh.minCount, Literal(1)))
g.add((p_theme, sh.maxCount, Literal(1)))

# the parameter shape
ds = arcgis.InSurfaceRasterShape
g.add((ds, RDF.type, sh.NodeShape))
g.add((ds, sh.targetNode, arcgis.in_surface_raster))
g.add((ds, sh.description, Literal('Constraints for ArcGIS tool Flow Direction', lang='en')))

p1 = BNode()
g.add((p1, sh.path, data.hasData))
g.add((p1, sh.minCount, Literal(1)))
g.add((p1, sh.maxCount, Literal(1)))
g.add((p1, sh['class'], data.RasterData))
g.add((p1,sh.node,''))
g.add((p1, sh.message, Literal('parameter in_surface_raster must has only 1 raster input dataset', lang='en')))
g.add((ds, sh.property, p1))



# save as turtle file
g.serialize('../shapes/case1_shapes.ttl', format='turtle')
