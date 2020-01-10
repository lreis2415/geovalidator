#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/9 17:21
from metadata import GeoMetadata
import pprint

r_file = '../data/dem_zts_84.tif'
v_file = '../data/ztsnet.shp'
v_file_w = '../data/ztswshed.shp'

def test_metadata():
	line_metadata = GeoMetadata.vector_metadata(v_file, 'streamnet')
	pprint.pprint(line_metadata)
	poly_metadata = GeoMetadata.vector_metadata(v_file_w, 'watershed')
	pprint.pprint(poly_metadata)
	dem_metadata = GeoMetadata.raster_metadata(r_file, 'DEM')
	pprint.pprint(dem_metadata)
