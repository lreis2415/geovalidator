#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/9 14:12

from osgeo import gdal, ogr
from os import path
from rdflib import Graph, BNode, Namespace, Literal, XSD, RDF
from rdflib.collection import Collection

# gdal/ogr readable file formats
gdal_drivers = {'vrt': 'VRT', 'tif': 'GTiff', 'ntf': 'NITF', 'toc': 'RPFTOC', 'xml': 'ECRGTOC', 'img': 'SRP', 'gff': 'GFF', 'asc': 'AAIGrid', 'ddf': 'SDTS', 'png': 'PNG',
                'jpg': 'JPEG', 'mem': 'JDEM', 'gif': 'BIGGIF', 'n1': 'ESAT', 'xpm': 'XPM', 'bmp': 'BMP', 'pix': 'PCIDSK', 'map': 'PCRaster', 'mpr/mpl': 'ILWIS', 'rgb': 'SGI',
                'hgt': 'SRTMHGT', 'ter': 'Terragen', 'nc': 'netCDF', 'hdf': 'HDF4', 'jp2': 'JP2OpenJPEG', 'grb': 'GRIB', 'rsw': 'RMF', 'nat': 'MSGN', 'rst': 'RST',
                'grd': 'NWT_GRD', 'hdr': 'SNODAS', 'rda': 'R', 'sqlite': 'Rasterlite', 'mbtiles': 'MBTiles', 'pnm': 'PNM', 'bt': 'BT', 'lcp': 'LCP', 'gtx': 'GTX', 'gsb': 'NTv2',
                'ACE2': 'ACE2', 'kro': 'KRO', 'rik': 'RIK', 'dem': 'USGSDEM', 'gxf': 'GXF', 'kea': 'KEA', 'hdf5': 'HDF5', 'grc': 'NWT_GRC', 'gen': 'ADRG', 'blx': 'BLX',
                'sdat': 'SAGA', 'xyz': 'XYZ', 'hf2': 'HF2', 'e00': 'E00GRID', 'dat': 'ZMap', 'bin': 'NGSGEOID', 'ppi': 'IRIS', 'prf': 'PRF', 'gpkg': 'GPKG', 'dwg': 'CAD'}
ogr_drivers = {'pix': 'PCIDSK', 'nc': 'netCDF', 'jp2': 'JP2OpenJPEG', 'shp': 'ESRI Shapefile', '000': 'S57', 'dgn': 'DGN', 'vrt': 'OGR_VRT', 'rec': 'REC', 'bna': 'BNA',
               'csv': 'CSV',
               'xml': 'NAS', 'gml': 'GML', 'gpx': 'GPX', 'kml': 'KML', 'gmt': 'OGR_GMT', 'gpkg': 'GPKG', 'map': 'WAsP', 'mdb': 'Geomedia', 'gdb': 'OpenFileGDB', 'dat': 'XPlane',
               'dxf': 'DXF',
               'dwg': 'CAD', 'vfk': 'VFK', 'thf': 'EDIGEO', 'svg': 'SVG', 'vct': 'Idrisi', 'xls': 'XLS', 'ods': 'ODS', 'xlsx': 'XLSX', 'sxf': 'SXF', 'jml': 'JML', 'e00': 'AVCE00'}


class Utils(object):
	@staticmethod
	def detect_data_type(file):
		"""
		test and return data type
		:param file: input data file
		:return: 0 raster; 1 vector; 2 general (non-geospatial)
		"""
		if not (path.exists(file) or path.isfile(file)):
			raise FileNotFoundError
		ext = path.splitext(file)[1].lower()
		if gdal_drivers.get(ext) is not None:
			ds = gdal.Open(file)
			if ds is None:
				raise ValueError('Invalid raster input data')
			# raster data
			return 0
		elif ogr_drivers.get(ext) is not None:
			ds = ogr.Open(file)
			if ds is None:
				# non-geospatial data
				if Utils.valid_file(file):
					return 2  # a valida file but invalid vector file
				else:
					raise ValueError('Invalid vector input data')
			# vector data
			return 1
		else:
			# non-geospatial data
			return 2

	@staticmethod
	def normalize(string: str):
		string = string.replace(' ', '_')
		return string

	@staticmethod
	def format_double(num, digital):
		return format(num, '.' + str(digital) + 'f')

	@staticmethod
	def valid_file(file):
		with open(file, 'r') as f:
			if len(f.readline(1)) > 0:
				return True
			else:
				return False

	@staticmethod
	def values_collection(graph, value_list: list):
		"""
		convert value list to rdflib collection
		:param graph: rdflib graph
		:param value_list: a list of values
		:return:
			graph, collection, list_node(BNode)
		"""
		list_node = BNode()
		coll = Collection(graph, list_node, value_list)
		return graph, coll, list_node

	@staticmethod
	def shacl_prefix(graph, prefix, namespace):
		sh = Namespace("http://www.w3.org/ns/shacl#")
		graph.bind('sh', sh)
		pre_node = BNode()
		graph.add((pre_node, sh.prefix, Literal(prefix)))
		graph.add((pre_node, sh.namespace, Literal(namespace, datatype=XSD.anyURI)))
		return graph, pre_node

	@staticmethod
	def shacl_prefixes(graph, sparql, prefix_tuples: list):
		"""
		add prefix declarations to sparql shape
		:param graph: rdflib graph
		:param sparql:  sparql query **BNode**
		:param prefix_tuples: [(prefix1,namespace1),(prefix2,namespace2)]
		:return: graph, sparql
		"""
		sh = Namespace("http://www.w3.org/ns/shacl#")
		graph.bind('sh', sh)
		prefixes = BNode()
		graph.add((prefixes, RDF.type, sh.PrefixDeclaration))
		for prefix_tuple in prefix_tuples:
			pre_node = BNode()
			graph.add((pre_node, sh.prefix, Literal(prefix_tuple[0])))
			graph.add((pre_node, sh.namespace, Literal(prefix_tuple[1], datatype=XSD.anyURI)))
			graph.add((prefixes, sh.declare, pre_node))
		graph.add((sparql, sh.prefixes, prefixes))
		return graph, sparql
