#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/9 17:00

from datagraph import DataGraph
import pprint

points = '../data/Heihe_Meteorology_Station_Distribution.shp'
basin = '../data/Heihe_Basin_Boundary_2010.shp'
dem_84 = '../data/dem_zts_84.tif'


def to_graph():
	dg = DataGraph()
	g1 = dg.vector_graph('clip_features', points, 'Meteorology_Station')
	# pprint.pprint(DataGraph.graph_2_string(g1))
	DataGraph.graph_2_file(g1, '../data_graphs/L7_clip_point.ttl')
	g2 = dg.vector_graph('in_features', basin, 'Basin')
	# pprint.pprint(DataGraph.graph_2_string(g2))
	DataGraph.graph_2_file(g2, '../data_graphs/L7_input_polygon.ttl')

	#----------------------------------------------------
	# g10 = dg.vector_graph('clip_features', streams, 'Streams')
	# pprint.pprint(DataGraph.graph_2_string(g10))
	# DataGraph.graph_2_file(g10, '../data_graphs/L7_clip_line_no_epsg.ttl')

	g11 = dg.vector_graph('in_features', points, 'Meteorology_Station')
	# pprint.pprint(DataGraph.graph_2_string(g11))
	DataGraph.graph_2_file(g11, '../data_graphs/L7_input_point.ttl')
	g22 = dg.vector_graph('clip_features', basin, 'Basin')
	# pprint.pprint(DataGraph.graph_2_string(g2))
	DataGraph.graph_2_file(g22, '../data_graphs/L7_clip_polygon.ttl')

	#-------------------------------------------------
	g3 = dg.raster_graph('input_raster', dem_84, 'DEM')
	# pprint.pprint(DataGraph.graph_2_string(g3))
	DataGraph.graph_2_file(g3, '../data_graphs/L9_input_dem.ttl')


if __name__ == '__main__':
	to_graph()
