#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 15:47

from rdflib import BNode, Graph, RDF, Literal, XSD
from rdflib.namespace import DCTERMS
from utils import Utils, DATA, SH, GEO, SF

g = Graph()
# prefixes
g.bind('data', DATA)
g.bind('sh', SH)
g.bind('geo', GEO)
g.bind('sf', SF)
g.bind('dcterms', DCTERMS)

# constraints for CRS
srk = DATA.CRSExistenceShape
g.add((srk, RDF.type, SH.NodeShape))
# property
p0 = BNode()
p00 = BNode()
g, c, l = Utils.values_collection(g, [DATA.hasCRS, DATA.hasEPSG])
g.add((p00, SH.alternativePath, l))
g.add((p0, SH.path, p00))
g.add((p0, SH.minCount, Literal(1)))
g.add((p0, SH.maxCount, Literal(1)))
g.add((p0, SH.datatype, XSD.string))
g.add((p0, SH.minLength, Literal(3)))
g.add((p0, SH.description, Literal('Checks whether a data set has a CRS.', lang='en')))
g.add((p0, SH.message, Literal('Vector must have a CRS.', lang='en')))
g.add((srk, SH.property, p0))

# SHACL shape graph
es = DATA.EPSGShape
g.add((es, RDF.type, SH.NodeShape))
g.add((es, SH.targetObjectsOf, DATA.hasEPSG))
g.add((es, SH.message,
       Literal('Invalid EPSG code! Must match the pattern ‘urn:ogc:def:crs:EPSG:[version]:[code]’,  ‘http://www.opengis.net/def/crs/EPSG/[version]/[code]’, or ‘EPSG:[code]’',
               lang='en')))
g.add((es, SH.datatype, XSD.string))
g.add((es, SH.minLength, Literal(9)))
g.add((es, SH.pattern, Literal('^(urn:ogc:def:crs:EPSG:[0-9.]{1,7}:[0-9]{4,5})|^(http://www.opengis.net/def/crs/EPSG/[0-9.]{1,7}/[0-9]{4,5})|^(EPSG:[0-9]{4,5})')))
g.add((es, SH.flag, Literal('i')))

# save as turtle file
g.serialize('../shapes/L4_CRSShape.ttl', format='turtle')
