#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 15:47

from rdflib import BNode, Graph, RDF, Namespace, Literal, XSD

g = Graph()
# namespaces
data = Namespace("http://www.egc.org/ont/data#")
arcgis = Namespace("http://www.egc.org/ont/process/arcgis#")
sh = Namespace("http://www.w3.org/ns/shacl#")
geo = Namespace('http://www.opengis.net/ont/geosparql#')
sf = Namespace('http://www.opengis.net/ont/sf#')
# prefixes
g.bind('data', data)
g.bind('sh', sh)
g.bind('arcgis', arcgis)
g.bind('geo', geo)
g.bind('sf', sf)
# SHACL shape graph

inf = arcgis.para_clip_features
g.add((inf, RDF.type, sh.NodeShape))
g.add((inf, RDF.type, arcgis.ArcGISInput))
g.add((inf, sh.targetNode, arcgis.para_clip_features_data))
g.add((inf, sh.minCount, Literal(1)))
g.add((inf, sh.maxCount, Literal(1)))
g.add((inf, sh.description, Literal('Parameter clip_features: the features to clip input features in ArcGIS Clip analysis', lang='en')))
g.add((inf, sh.node, data.VectorDataEPSGShape))

# SPARQL shape
sparql = BNode()
g.add((sparql, sh.message, Literal(
	'Clip features cannot be used to clip input features. When the Input Features are polygons, the Clip Features must also be polygons. When the Input Features are lines, the Clip Features can be lines or polygons. When the Input Features are points, the Clip Features can be points, lines, or polygons.',
	lang='en')))

pre_geo = BNode()
g.add((pre_geo, sh.prefix, Literal('geo')))
g.add((pre_geo, sh.namespace, Literal('http://www.opengis.net/ont/geosparql#', datatype=XSD.anyURI)))
pre_arcgis = BNode()
g.add((pre_arcgis, sh.prefix, Literal('arcgis')))
g.add((pre_arcgis, sh.namespace, Literal('http://www.egc.org/ont/process/arcgis#', datatype=XSD.anyURI)))
pre_sf = BNode()
g.add((pre_sf, sh.prefix, Literal('sf')))
g.add((pre_sf, sh.namespace, Literal('http://www.opengis.net/ont/sf#', datatype=XSD.anyURI)))

prefixes = BNode()
g.add((prefixes, RDF.type, sh.PrefixDeclaration))
g.add((prefixes, sh.declare, pre_geo))
g.add((prefixes, sh.declare, pre_arcgis))
g.add((prefixes, sh.declare, pre_sf))
g.add((sparql, sh.prefixes, prefixes))

query = """
SELECT $this (geo:hasGeometry AS ?path) (?clip_geom AS ?value)
	WHERE {
		$this geo:hasGeometry ?clip_geom.
        arcgis:para_in_features geo:hasGeometry ?in_geom.
		FILTER ( 
			IF(?in_geom a sf:Point,true,false)||
            IF((?in_geom a sf:Line) && not(?clip_geom a sf:Point),true,false)||
            IF((?in_geom a sf:Polygon) && (?clip_geom a sf:Polygon),true,false)). 
        }
"""
g.add((sparql, sh.select, Literal(query)))
g.add((inf, sh.sparql, sparql))

# save as turtle file
g.serialize('../shapes/L7_SparqlShape.ttl', format='turtle')
