#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/5 17:21
from osgeo import gdal, ogr, osr
from os import path

class GeoMetadata(object):

	@staticmethod
	def vector_metadata(data, data_theme=None):
		"""

		Args:
			data: input data
			data_theme: data theme of input data

		Returns:
			metadata

		"""
		ds = ogr.Open(data)
		if ds is None:
			raise ValueError('Invalid vector data')
		metadata = dict()
		metadata['content'] = path.basename(data)
		# 数据驱动名称，数据格式
		metadata['format'] = ds.GetDriver().name
		layer = ds.GetLayer(0)
		# 空间参考
		srs = layer.GetSpatialRef()
		# proj4 格式
		metadata['proj4'] = srs.ExportToProj4()
		# well known text 格式
		metadata['wkt'] = srs.ExportToWkt()
		metadata['theme'] = data_theme
		# 地理坐标系
		metadata['geogcs'] = srs.GetAttrValue('GEOGCS')
		metadata['uom'] = srs.GetAttrValue('UNIT')
		# 投影坐标系
		metadata['projcs'] = srs.GetAttrValue('PROJCS')  # if projected
		# EPSG 代码
		metadata['epsg'] = srs.GetAuthorityCode(None)
		feature = layer.GetNextFeature()
		geom = feature.GetGeometryRef()
		if geom.GetGeometryName() == 'LINESTRING':
			metadata['geometry'] = 'LineString'
		else:
			metadata['geometry'] = geom.GetGeometryName().capitalize()
		metadata['featureCount'] = layer.GetFeatureCount()
		# 是否有投影
		metadata['isProjected'] = srs.IsProjected()
		# 范围：minX, maxX, minY, maxY
		env = geom.GetEnvelope()
		# envelope：一般是 xmin,  ymin,  xmax,  ymax
		metadata['extent'] = env  # [env[0], env[2], env[1], env[3]]
		# 中心点，不一定在图形内部
		cid = geom.Centroid()
		metadata['centroid'] = [cid.GetX(), cid.GetY()]
		ds = None
		return metadata

	@staticmethod
	def raster_metadata(data, data_theme=None):
		"""

		Args:
			data: input data
			data_theme: data theme of input data

		Returns:
			metadata

		"""
		ds = gdal.Open(data)
		if ds is None:
			raise ValueError('Invalid raster data')
		metadata = dict()
		metadata['content'] = path.basename(data)
		# 也可以是 LongName。GTiff 与 GeoTiff 的区别
		metadata['format'] = ds.GetDriver().ShortName
		# 波段数
		metadata['band_count'] = ds.RasterCount
		# band 1
		band = ds.GetRasterBand(1)
		metadata['nodata'] = band.GetNoDataValue()
		# 统计值
		band_stat = band.GetStatistics(True, True)
		metadata['min'] = band_stat[0]
		metadata['max'] = band_stat[1]
		metadata['mean'] = band_stat[2]
		metadata['stddev'] = band_stat[3]
		metadata['theme'] = data_theme
		# 空间参考系统
		srs = osr.SpatialReference(ds.GetProjectionRef())
		metadata['proj4'] = srs.ExportToProj4()
		metadata['wkt'] = srs.ExportToWkt()
		# 地理坐标系
		metadata['geogcs'] = srs.GetAttrValue('GEOGCS')
		metadata['uom'] = srs.GetAttrValue('UNIT')
		# 投影坐标系
		metadata['projcs'] = srs.GetAttrValue('PROJCS')  # if projected
		# if srs.GetAttrValue('Authority', 0) == 'EPSG':
		metadata['epsg'] = srs.GetAttrValue('Authority', 1)
		# metadata['epsg'] = srs.GetAuthorityCode(None)
		# metadata['srid'] = srs.GetAttrValue('AUTHORITY', 1)
		# 是否有地图投影（平面坐标）
		metadata['isProjected'] = srs.IsProjected()
		# 仿射变换信息，6参数：
		# upper left x, x(w-e) resolution, x skew, upper left y, y skew, y(s-n) resolution
		ulx, xres, xskew, uly, yskew, yres = ds.GetGeoTransform()
		lrx = ulx + (ds.RasterXSize * xres)  # low right x
		lry = uly + (ds.RasterYSize * yres)  # low right y

		metadata['minx'] = ulx
		maxx = lrx  # ulx + xres * ds.RasterXSize
		metadata['maxx'] = maxx
		miny = lry  # uly + yres * ds.RasterYSize
		metadata['miny'] = miny
		metadata['maxy'] = uly
		# 中心点 centroid
		cx = ulx + xres * (ds.RasterXSize / 2)
		cy = uly + yres * (ds.RasterYSize / 2)

		# metadata['central_x'] = cx
		# metadata['central_y'] = cy
		metadata['resolution'] = xres
		# geographic width
		metadata['width'] = ds.RasterXSize * xres
		# geographic height，negative，负值
		metadata['height'] = ds.RasterYSize * yres
		# image width
		metadata['size_width'] = ds.RasterXSize
		metadata['size_height'] = ds.RasterYSize
		# minx,miny,maxx,maxy
		metadata['extent'] = [ulx, miny, maxx, uly]
		metadata['centroid'] = [cx, cy]
		ds = None
		return metadata
