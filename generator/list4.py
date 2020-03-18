#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 15:47

from rdflib import BNode, Graph, RDF, Namespace, Literal, XSD
from rdflib.namespace import DCTERMS
from utils import Utils

g = Graph()
# namespaces
data = Namespace("http://www.egc.org/ont/data#")
sh = Namespace("http://www.w3.org/ns/shacl#")
geo = Namespace('http://www.opengis.net/ont/geosparql#')
sf = Namespace('http://www.opengis.net/ont/sf#')
# prefixes
g.bind('data', data)
g.bind('sh', sh)
g.bind('geo', geo)
g.bind('sf', sf)
g.bind('dcterms', DCTERMS)

# constraints for CRS
srk = data.CRSExistenceShape
g.add((srk, RDF.type, sh.NodeShape))
# property
p0 = BNode()
p00 = BNode()
g, c, l = Utils.values_collection(g, [data.hasCRS, data.hasEPSG])
g.add((p00, sh.alternativePath, l))
g.add((p0, sh.path, p00))
g.add((p0, sh.minCount, Literal(1)))
g.add((p0, sh.maxCount, Literal(1)))
g.add((p0, sh.datatype, XSD.string))
g.add((p0, sh.minLength, Literal(3)))
g.add((p0, sh.description, Literal('Checks whether a data set has a CRS.', lang='en')))
g.add((srk, sh.property, p0))

# SHACL shape graph
es = data.EPSGShape
g.add((es, RDF.type, sh.NodeShape))
g.add((es, sh.targetObjectsOf, data.hasEPSG))
g.add((es, sh.message,
       Literal('Invalid EPSG code! Must match the pattern ‘urn:ogc:def:crs:EPSG:[version]:[code]’,  ‘http://www.opengis.net/def/crs/EPSG/[version]/[code]’, or ‘EPSG:[code]’',
               lang='en')))
g.add((es, sh.datatype, XSD.string))
g.add((es, sh.minLength, Literal(9)))
g.add((es, sh.pattern, Literal('^(urn:ogc:def:crs:EPSG:[0-9.]{,7}:[0-9]{4,5})|^(http://www.opengis.net/def/crs/EPSG/[0-9.]{1,7}/[0-9]{4,5})|^(EPSG:[0-9]{4,5}')))
g.add((es, sh.flag, Literal('i')))

# save as turtle file
g.serialize('../shapes/L4_CRSShape.ttl', format='turtle')
