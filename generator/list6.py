#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 15:47

from rdflib import BNode, Graph, RDF, Namespace, Literal
from rdflib.namespace import DCTERMS
from utils import Utils

g = Graph()
# namespaces
data = Namespace("http://www.egc.org/ont/data#")
arcgis = Namespace("http://www.egc.org/ont/process/arcgis#")
sh = Namespace("http://www.w3.org/ns/shacl#")
geo = Namespace('http://www.opengis.net/ont/geosparql#')
sf = Namespace('http://www.opengis.net/ont/sf#')
process = Namespace("http://www.egc.org/ont/process#")
# prefixes
g.bind('data', data)
g.bind('sh', sh)
g.bind('arcgis', arcgis)
g.bind('geo', geo)
g.bind('sf', sf)
g.bind('process', process)
g.bind('dcterms', DCTERMS)
# functionality-level
cap = arcgis.ClipAnalysisShape
g.add((cap, RDF.type, sh.NodeShape))
g.add((cap, sh.targetNode, arcgis.clip_analysis))
msg1 = 'Must have exactly one input value with identifier ' \
       '‘in_features’ for parameter ‘in_features’ of tool ‘Clip_analysis’'
cap = Utils.parameter_qualified_value_shape(g, cap, process.hasInputData, 'in_features', msg1)

msg2 = 'Must have exactly one input value with identifier ' \
       '‘clip_features’ for parameter ‘clip_features’ of tool ‘Clip_analysis’'
cap = Utils.parameter_qualified_value_shape(g, cap, process.hasInputData, 'clip_features', msg2)

# SHACL shape graph

inf = arcgis.clip_features
g.add((inf, RDF.type, sh.NodeShape))
g.add((inf, RDF.type, arcgis.ArcGISInput))
g.add((inf, sh.targetNode, data.clip_features_data))
g.add((inf, sh.description, Literal('Parameter clip_features: the features to clip input features in ArcGIS Clip analysis', lang='en')))
g.add((inf, sh.node, data.VectorDataShape))

# SPARQL shape
sparql_geom = BNode()
sparql_geom = Utils.shacl_prefixes(g, sparql_geom,
                                      [('geo', geo), ('sf', sf), ('data', data)])

g.add((sparql_geom, sh.message, Literal(
	'Clip features cannot be used to clip input features. When the Input Features are polygons, the Clip Features must also be polygons. When the Input Features are lines, the Clip Features can be lines or polygons. When the Input Features are points, the Clip Features can be points, lines, or polygons.',
	lang='en')))

query = """
SELECT $this (geo:hasGeometry AS ?path) (?clip_geom AS ?value)
	WHERE {
		$this geo:hasGeometry ?clip_geom.
        data:in_features_data geo:hasGeometry ?in_geom.
		FILTER ( 
			IF(EXISTS {?in_geom a sf:Point},false,true)||
            IF(EXISTS {?in_geom a sf:Line} && NOT EXISTS {?clip_geom a sf:Point},false,true)||
            IF(EXISTS {?in_geom a sf:Polygon} && EXISTS {?clip_geom a sf:Polygon},false,true)). 
        }
"""
g.add((sparql_geom, sh.select, Literal(query)))
g.add((inf, sh.sparql, sparql_geom))
# ----------------------------------------------------
query_crs = """
SELECT $this (data:hasEPSG AS ?path) (?clip_epsg AS ?value)
	WHERE {
		$this data:hasEPSG ?clip_epsg.
        data:in_features_data data:hasEPSG ?in_epsg.
		FILTER (?in_epsg !=?clip_epsg). 
        }
"""
sparql_crs = BNode()
sparql_crs = Utils.shacl_prefixes(g, sparql_crs, [('data', data)])
g.add((sparql_crs, sh.message, Literal(
	'Input Features and Clip Features must have the same coordinate system.',
	lang='en')))
g.add((sparql_crs, sh.select, Literal(query_crs)))
g.add((inf, sh.sparql, sparql_crs))

# save as turtle file
g.serialize('../shapes/L6_SparqlShape.ttl', format='turtle')
