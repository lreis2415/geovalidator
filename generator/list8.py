#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 15:47

from rdflib import BNode, Graph, RDF, Namespace, Literal
from utils import Utils

g = Graph()
# namespaces
data = Namespace("http://www.egc.org/ont/data#")
process = Namespace("http://www.egc.org/ont/process#")
arcgis = Namespace("http://www.egc.org/ont/process/arcgis#")
sh = Namespace("http://www.w3.org/ns/shacl#")
geo = Namespace('http://www.opengis.net/ont/geosparql#')
sf = Namespace('http://www.opengis.net/ont/sf#')
# prefixes
g.bind('data', data)
g.bind('sh', sh)
g.bind('arcgis', arcgis)
g.bind('process', process)

# a SHACL triple rule
rrs = data.ProjectVectorCGCS2000Rule
g.add((rrs, RDF.type, sh.NodeShape))
g.add((rrs, sh.targetClass, data.VectorData))
g.add((rrs, sh.description,
       Literal('For all vector data, if their CRS is not CGCS 2000 (EPSG:4490),'
               ' the ‘project’ tool will be inferred as a pre-processing tool for the data', lang='en')))

rule = BNode()
g.add((rule, RDF.type, sh.SPARQLRule))
g.add((rule, sh.node, data.VectorDataShape))
# sparql conditions
rule = Utils.shacl_prefixes(g, rule, [('data', data),('process',process),('arcgis',arcgis)])
sparql = """
       CONSTRUCT {
              $this process:isInputDataOf arcgis:project. # pre-processing
              # also need a custome geographic transformation
              arcgis:project process:from arcgis:create_custome_geographic_transformation.
       }
       # condition expressed using SPARQL 
       WHERE {
              $this data:hasEPSG|data:hasCRS ?epsg .
              FILTER (?epsg != “EPSG:4490”)
       }
       """

g.add((rule, sh.construct ,Literal(sparql)))
g.add((rrs, sh.rule, rule))

# save as turtle file
g.serialize('../shapes/L8_TripleRule.ttl', format='turtle')
