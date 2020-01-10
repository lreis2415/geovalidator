#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 16:10

from rdflib import BNode, Graph, RDF, Namespace, Literal
from rdflib.collection import Collection

g = Graph()
# namespaces
data = Namespace("http://www.egc.org/ont/data#")
arcgis = Namespace("http://www.egc.org/ont/process/arcgis#")
taudem = Namespace("http://www.egc.org/ont/process/taudem#")
sh = Namespace("http://www.w3.org/ns/shacl#")
geo = Namespace('http://www.opengis.net/ont/geosparql#')
sf = Namespace('http://www.opengis.net/ont/sf#')
gcmd = Namespace('https://gcmdservices.gsfc.nasa.gov/kms/concept/')
dta = Namespace('http://www.egc.org/ont/domain/dta#')
ogc = Namespace('http://www.egc.org/ont/vocab/ogc#')
# prefixes
g.bind('data', data)
g.bind('sh', sh)
g.bind('arcgis', arcgis)
g.bind('geo', geo)
g.bind('sf', sf)
g.bind('gcmd', gcmd)
g.bind('dta', dta)
g.bind('ogc', ogc)
g.bind('taudem', taudem)
# SHACL shape graph
ds = data.DEMDataShape
g.add((ds, RDF.type, sh.NodeShape))
p = BNode()
l = BNode()
c = Collection(g, l, [gcmd.dem, dta.DEM, ogc.DigitalElevationModel])
# print(c[0])
g.add((p, sh.path, data.dataTheme))
g.add((p, sh['in'], l))
g.add((p, sh.minCount, Literal(1)))
g.add((p, sh.maxCount, Literal(1)))
g.add((p, sh.message, Literal('Only supports Digital Elevation Model (DEM) data', lang='en')))
g.add((ds, sh.property, p))

ies = data.InputElevationShape
g.add((ies, RDF.type, sh.NodeShape))
g.add((ies, sh.targetNode, taudem.Input_Elevation_Grid))
g.add((ies, sh.targetNode, taudem.Input_DEM_Dataset))
g.add((ies, sh.node, data.DEMDataShape))

p2 = BNode()
g.add((p2, sh.path, data.dataFormat))
g.add((p2, sh['class'], data.GDALRasterFormat))
g.add((p2, sh.minCount, Literal(1)))
g.add((p2, sh.maxCount, Literal(1)))
g.add((p2, sh.defaultValue, data.GTiff))
g.add((ies, sh.property, p2))

# save as turtle file
g.serialize('../shapes/L2_DEMDataShape.ttl', format='turtle')
