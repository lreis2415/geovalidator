#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/9 17:00

from datagraph import DataGraph
import pprint

linestring = '../data/ztsnet.shp'
linestring_no_epsg = '../data/ztsnet_no_epsg.shp'
polygon = '../data/ztswshed.shp'
dem_84 = '../data/dem_zts_84.tif'
dem = '../data/dem_zts_noproj.tif'


def to_graph():
	dg = DataGraph()
	g1 = dg.vector_graph('para_clip_features', linestring, 'StreamNet')
	# pprint.pprint(DataGraph.graph_2_string(g1))
	DataGraph.graph_2_file(g1, '../data_graphs/L7_clip_line.ttl')

	g10 = dg.vector_graph('para_clip_features', linestring, 'StreamNet')
	# pprint.pprint(DataGraph.graph_2_string(g10))
	DataGraph.graph_2_file(g10, '../data_graphs/L7_clip_line_no_epsg.ttl')

	g2 = dg.vector_graph('para_in_features', polygon, 'Watershed')
	# pprint.pprint(DataGraph.graph_2_string(g2))
	DataGraph.graph_2_file(g2, '../data_graphs/L7_input_polygon.ttl')

	g11 = dg.vector_graph('para_in_features', linestring, 'StreamNet')
	# pprint.pprint(DataGraph.graph_2_string(g11))
	DataGraph.graph_2_file(g11, '../data_graphs/L7_input_line.ttl')

	g3 = dg.raster_graph('inputRaster', dem, 'DEM')
	# pprint.pprint(DataGraph.graph_2_string(g3))
	DataGraph.graph_2_file(g3, '../data_graphs/L9_input_dem.ttl')


if __name__ == '__main__':
	to_graph()
