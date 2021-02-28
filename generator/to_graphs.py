#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/9 17:00

from datagraph import DataGraph
from utils import ArcGIS

points = '../data/Heihe_Meteorology_Station_Distribution.shp'
basin = '../data/Heihe_Basin_Boundary_2010.shp'
dem = '../data/ywzdem30m.tif'

def to_graph():
	dg = DataGraph()
	g1 = dg.vector_graph(ArcGIS,'clip_features', points, 'Meteorology_Station')
	DataGraph.graph_2_file(g1, '../data_graphs/L6_clip_point.ttl')
	g2 = dg.vector_graph(ArcGIS,'in_features', basin, 'Basin')
	DataGraph.graph_2_file(g2, '../data_graphs/L6_input_polygon.ttl')

	#----------------------------------------------------
	g11 = dg.vector_graph(ArcGIS,'in_features', points, 'Meteorology_Station')
	DataGraph.graph_2_file(g11, '../data_graphs/L6_input_point.ttl')
	g22 = dg.vector_graph(ArcGIS,'clip_features', basin, 'Basin')
	DataGraph.graph_2_file(g22, '../data_graphs/L6_clip_polygon.ttl')

	#-------------------------------------------------
	g3 = dg.raster_graph(ArcGIS,'in_surface_raster', dem, 'DEM')
	DataGraph.graph_2_file(g3, '../data_graphs/L8_input_raster.ttl')


if __name__ == '__main__':
	to_graph()
