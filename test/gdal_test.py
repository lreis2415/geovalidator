#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/8 22:58
from osgeo import gdal

r_file = '../data/dem_zts_84.tif'
v_file = '../data/ztsnet.shp'
g_file = 'for_test.txt'
g_file2 = '../ont/QUDT ALL UNITS.ttl'
x_file = '../data/dem_zts_noproj.tif.aux.xml'
x_file2 = 'for_test.xml'
gdal.UseExceptions()


def gdal_error_handler(err_class, err_num, err_msg):
	errtype = {
		gdal.CE_None: 'None',
		gdal.CE_Debug: 'Debug',
		gdal.CE_Warning: 'Warning',
		gdal.CE_Failure: 'Failure',
		gdal.CE_Fatal: 'Fatal'
		}
	err_msg = err_msg.replace('\n', ' ')
	err_class = errtype.get(err_class, 'None')
	print('Error Number: %s' % (err_num))
	print('Error Type: %s' % (err_class))
	print('Error Message: %s' % (err_msg))


# gdal.PushErrorHandler(gdal_error_handler)

from utils import Utils


def test_data_type():
	print(Utils.detect_data_type(x_file2))
	print(Utils.detect_data_type(g_file))
