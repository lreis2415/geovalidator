#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 15:47

from rdflib import BNode, Graph, RDF, Literal
from rdflib.namespace import DCTERMS
from utils import Utils, DATA, ArcGIS, GEO, SH, PROCESS, SF

g = Graph()
# vector data shape
g.parse('../shapes/L5_VectorDataShape.ttl', format='turtle')

# prefixes
g.bind('data', DATA)
g.bind('sh', SH)
g.bind('arcgis', ArcGIS)
g.bind('geo', GEO)
g.bind('sf', SF)
g.bind('process', PROCESS)
g.bind('dcterms', DCTERMS)
# functionality-level
cap = ArcGIS.ClipAnalysisShape
g.add((cap, RDF.type, SH.NodeShape))
g.add((cap, SH.targetNode, ArcGIS.clip_analysis))
msg1 = 'Must have exactly one input with identifier ' \
       '‘in_features’ for parameter ‘in_features’ of tool ‘Clip_analysis’'
cap = Utils.parameter_qualified_value_shape(g, cap, PROCESS.hasInputData, 'in_features', msg1)

msg2 = 'Must have exactly one input value with identifier ' \
       '‘clip_features’ for parameter ‘clip_features’ of tool ‘Clip_analysis’'
cap = Utils.parameter_qualified_value_shape(g, cap, PROCESS.hasInputData, 'clip_features', msg2)

# SHACL shape graph
inf = ArcGIS.clip_features
g.add((inf, RDF.type, SH.NodeShape))
g.add((inf, RDF.type, ArcGIS.ArcGISInput))
g.add((inf, SH.targetNode, DATA.clip_features_data))
g.add((inf, SH.description, Literal('Parameter clip_features: the features to clip input features in ArcGIS Clip analysis', lang='en')))
g.add((inf, SH.node, DATA.VectorDataShape))

# SPARQL shape
sparql_geom = BNode()
sparql_geom = Utils.shacl_prefixes(g, sparql_geom,
                                   [('geo', GEO), ('sf', SF), ('data', DATA)])

g.add((sparql_geom, SH.message, Literal(
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
query2 = """
SELECT $this (geo:hasGeometry AS ?path) (?clip_geom AS ?value)
	WHERE {
		$this geo:hasGeometry/a ?clip_geom.
        data:in_features_data geo:hasGeometry/a ?in_geom.
		FILTER ( 
			IF(?in_geom = sf:Point,false,true)||
            IF((?in_geom = sf:Line) && (?clip_geom != sf:Point),false,true)||
            IF((?in_geom = sf:Polygon) && (?clip_geom = sf:Polygon),false,true)). 
        }
"""
g.add((sparql_geom, SH.select, Literal(query2)))
g.add((inf, SH.sparql, sparql_geom))
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
sparql_crs = Utils.shacl_prefixes(g, sparql_crs, [('data', DATA)])
g.add((sparql_crs, SH.message, Literal(
	'Input Features and Clip Features must have the same coordinate system.',
	lang='en')))
g.add((sparql_crs, SH.select, Literal(query_crs)))

# save as turtle file
g.serialize('../shapes/L6_SparqlShape.ttl', format='turtle')
