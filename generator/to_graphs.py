#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/9 17:00

from datagraph import DataGraph

points = '../data/Heihe_Meteorology_Station_Distribution.shp'
basin = '../data/Heihe_Basin_Boundary_2010.shp'
dem_84 = '../data/dem_zts_84.tif'

def to_graph():
	dg = DataGraph()
	g1 = dg.vector_graph('clip_features', points, 'Meteorology_Station')
	DataGraph.graph_2_file(g1, '../data_graphs/L6_clip_point.ttl')
	g2 = dg.vector_graph('in_features', basin, 'Basin')
	DataGraph.graph_2_file(g2, '../data_graphs/L6_input_polygon.ttl')

	#----------------------------------------------------
	g11 = dg.vector_graph('in_features', points, 'Meteorology_Station')
	DataGraph.graph_2_file(g11, '../data_graphs/L6_input_point.ttl')
	g22 = dg.vector_graph('clip_features', basin, 'Basin')
	DataGraph.graph_2_file(g22, '../data_graphs/L6_clip_polygon.ttl')

	#-------------------------------------------------
	g3 = dg.raster_graph('input_raster', dem_84, 'DEM')
	DataGraph.graph_2_file(g3, '../data_graphs/L7_input_dem.ttl')


if __name__ == '__main__':
	to_graph()
