#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/4/27 13:23
from owlready2 import *
import json
import re
from JSON2OWL.OwlConvert.OwlUtils import OWLUtils

model_uri = 'http://www.egc.org/ont/process/test'
onto = get_ontology(model_uri)
onto, sh, skos, dcterms, props = OWLUtils.load_common(onto)
onto, gb, task, data, cyber = OWLUtils.load_common_for_process_tool(onto)
onto = OWLUtils.load_geo_vocabl(onto)
# onto, gcmd, csdms, cf, dta, hydrology, gis_vocab = OWLUtils.load_geo_vocabl(onto)
print('ontologies imported')


def search(word):
	word = word # 含空格
	print(onto.search(prefLabel ='*'+ word))
	# word = word.replace(' ', '_')
	# print(onto.search(label = "*"+word))

search('lake')

