#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/4 15:47

from rdflib import BNode, Graph, RDF, Namespace, Literal, XSD

g = Graph()
# namespaces
data = Namespace("http://www.egc.org/ont/data#")
process = Namespace("http://www.egc.org/ont/process#")
sh = Namespace("http://www.w3.org/ns/shacl#")
soft = Namespace("http://www.egc.org/ont/cyber#")

# prefixes
g.bind('data', data)
g.bind('sh', sh)
g.bind('process', process)
g.bind('soft', soft)
# SHACL shape graph

themeShape = process.DataThemePropertyShape
g.add((themeShape, RDF.type, sh.PropertyShape))
g.add((themeShape, sh.targetSubjectsOf, process.preprocessor))
g.add((themeShape, sh.path, data.dataTheme))

# SPARQL shape
sparql = BNode()
g.add((sparql, sh.message, Literal('Input data theme must consistent with output data theme of pre-processor.', lang='en')))

pre_process = BNode()
g.add((pre_process, sh.prefix, Literal('process')))
g.add((pre_process, sh.namespace, Literal('http://www.egc.org/ont/process#', datatype=XSD.anyURI)))
pre_soft = BNode()
g.add((pre_soft, sh.prefix, Literal('soft')))
g.add((pre_soft, sh.namespace, Literal('http://www.egc.org/ont/cyber#', datatype=XSD.anyURI)))

prefixes = BNode()
g.add((prefixes, RDF.type, sh.PrefixDeclaration))
g.add((prefixes, sh.declare, pre_process))
g.add((prefixes, sh.declare, pre_soft))
g.add((sparql, sh.prefixes, prefixes))

query = """
SELECT $this  (?in_theme AS ?value)
	WHERE {
		$this  soft:input  ?in_param. # input parameter
		?in_param  $PATH   ?in_theme.  # data theme of input parameter 
        $this  process:preprocessor  ?pre_func.   # preceding functionality
        ?pre_func soft:output  ?out_param.  #  output parameter
		?out_param  $PATH  ?out_theme.   #  data theme of output parameter
		FILTER (  ?in_theme = ?out_theme  ). # is equal
        }
"""
g.add((sparql, sh.select, Literal(query)))
g.add((themeShape, sh.sparql, sparql))

# save as turtle file
g.serialize('../shapes/L8_SparqlThemeShape.ttl', format='turtle')
