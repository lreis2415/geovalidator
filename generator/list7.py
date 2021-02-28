#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 15:47

from rdflib import BNode, Graph, RDF, Namespace, Literal, XSD
from utils import Utils

g = Graph()
# namespaces
data = Namespace("http://www.egc.org/ont/data#")
process = Namespace("http://www.egc.org/ont/process#")
sh = Namespace("http://www.w3.org/ns/shacl#")

# prefixes
g.bind('data', data)
g.bind('sh', sh)
g.bind('process', process)
# SHACL shape graph

themeShape = process.DataThemeShape
g.add((themeShape, RDF.type, sh.PropertyShape))
g.add((themeShape, sh.targetSubjectsOf, process.preprocessor))
g.add((themeShape, sh.path, data.dataTheme))

# SPARQL shape
sparql = BNode()

sparql = Utils.shacl_prefixes(g, sparql, [('process', process),  ('data', data)])
g.add((sparql, sh.message, Literal('Data theme (e.g., DEM ) of the output and input data of two functionalities that linked via process:preprocessor must be consistent.', lang='en')))

query = """
SELECT $this  (?in_theme AS ?value)
	WHERE {
		$this  process:hasInput/$PATH   ?in_theme.  # data theme of input parameter 
        $this  process:from  ?pre_func.   # preceding tool
        ?pre_func process:hasOutput/$PATH  ?out_theme.   #  data theme of output parameter
		FILTER (  ?in_theme != ?out_theme  ). # is not equal
        }
"""
g.add((sparql, sh.select, Literal(query)))
g.add((themeShape, sh.sparql, sparql))

# save as turtle file
g.serialize('../shapes/L7_DataThemeShape.ttl', format='turtle')
