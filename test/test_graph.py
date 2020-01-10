#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/8 16:38
# pytest
from datagraph import DataGraph
import pprint

file = '../data/dem_zts_84.tif'


def test_graph():
	dg = DataGraph()
	g = dg.raster_graph('dem', file, 'DEM')
	pprint.pprint(DataGraph.graph_2_string(g))
