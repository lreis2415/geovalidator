#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/5 18:02

from math import cos, sin, asin, sqrt, radians

from osgeo import gdal, osr, ogr



def test_dis():
	print(calc_distance(0, 0, 0.000243406343443, 0))
	srs = osr.SpatialReference()
	srs.ImportFromEPSG(4326)
	degree_2_meter(srs, 0, 0.00024340634344316355)



def calc_distance(lat1, lon1, lat2, lon2):
	"""
	计算大圆长
	https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
	Calculate the great circle distance between two points
	on the earth (specified in decimal degrees)
	"""
	# convert decimal degrees to radians
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	# haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = 0.5 - cos(dlat) / 2 + cos(lat1) * cos(lat2) * (1 - cos(dlon)) / 2
	# a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
	c = 2 * asin(sqrt(a))
	m = 6371 * c * 1000
	return m


def degree_2_meter(src_crs: osr.SpatialReference, x, y):
	target_crs = osr.SpatialReference()
	target_crs.ImportFromEPSG(3857)  # Web Mercator
	coordTrans = osr.CoordinateTransformation(src_crs, target_crs)
	geom = ogr.CreateGeometryFromWkt('POINT (' + str(x) + ' ' + str(y) + ')')
	geom.Transform(coordTrans)

	px = geom.GetX()
	py = geom.GetY()
	print(int(px))
	print(int(py))
