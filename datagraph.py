#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/5 18:01

import os, re
from rdflib import Graph, RDF, Namespace, Literal, XSD
from rdflib.namespace import DCTERMS, SKOS
from metadata import GeoMetadata
from utils import Utils


class DataGraph(object):
	def __init__(self):
		"""
		namespaces and bind prefixes
		"""
		self.sh = Namespace('http://www.w3.org/ns/shacl#')
		self.unit = Namespace('http://qudt.org/2.1/vocab/unit#')
		self.data_ns = Namespace('http://www.egc.org/ont/data#')
		self.soft = Namespace('http://www.egc.org/ont/gis/cyber#')
		self.geo = Namespace('http://www.opengis.net/ont/geosparql#')
		self.sf = Namespace('http://www.opengis.net/ont/sf#')
		self.dcterms = DCTERMS

		self.g = Graph()
		self.g.bind('data', self.data_ns)
		self.g.bind('sh', self.sh)
		self.g.bind('geo', self.geo)
		self.g.bind('sf', self.sf)
		self.g.bind('unit', self.unit)
		self.g.bind('dcterms', self.dcterms)

	@staticmethod
	def graph_2_string(graph):
		"""
		serialize RDF graph as string
		:param graph:
		:return: RDF string in turtle syntax
		"""
		content = graph.serialize(format='turtle')  # bytes
		return content.decode('utf-8')

	@staticmethod
	def graph_2_file(graph, file_path):
		"""
		save RDF graph as turtle file
		:param graph:
		:param file_path:
		:return: file path
		"""
		if not os.path.exists(os.path.dirname(file_path)):
			os.makedirs(file_path)
		graph.serialize(file_path, format='turtle')
		return file_path

	def _format(self, num):
		return format(num, '0.3f')

	def _literal(self, val, dtype):
		return Literal(val, datatype=dtype)

	def _get_uom(self, meta_uom):
		"""
		get unit of measure instance from QUDT ontology
		:param meta_uom:
		:return:
		"""
		if meta_uom.capitalize() == 'Degree':
			return self.unit.DEG
		elif meta_uom == 'meter' or meta_uom == 'metre':
			return self.unit.M
		else:
			unit_g = Graph()
			unit_g.parse("../ont/QUDT ALL UNITS.ttl", format="turtle")
			for uom in unit_g.subjects(SKOS.prefLabel, Literal(meta_uom)):
				return uom

	def _add_extent(self, g, node, minx, miny, maxx, maxy):
		minx = self._format(minx)
		miny = self._format(miny)
		maxx = self._format(maxx)
		maxy = self._format(maxy)
		data_ns = self.data_ns
		dtype = XSD.double
		g.add((node, data_ns.minX, Literal(minx, datatype=dtype)))
		g.add((node, data_ns.westBoundingCoordinate, Literal(minx, datatype=dtype)))
		g.add((node, data_ns.maxX, Literal(maxx, datatype=dtype)))
		g.add((node, data_ns.eastBoundingCoordinate, Literal(maxx, datatype=dtype)))
		g.add((node, data_ns.minY, Literal(miny, datatype=dtype)))
		g.add((node, data_ns.southBoundingCoordinate, Literal(miny, datatype=dtype)))
		g.add((node, data_ns.maxY, Literal(maxy, datatype=dtype)))
		g.add((node, data_ns.northBoundingCoordinate, Literal(maxy, datatype=dtype)))
		g.add((node, data_ns.spatialExtent, Literal(str(minx) + ',' + str(miny) + ',' + str(maxx) + ',' + str(maxy), datatype=XSD.string)))
		return g

	def vector_graph(self, parameter_id, data, data_theme=None):
		"""
		translate vector metadata into RDF graph
		Args:
			parameter_id: parameter identifier
			data: input data
			data_theme: data theme of input data

		Returns:
			graph

		"""
		metadata = GeoMetadata.vector_metadata(data, data_theme)
		# a new graph with everything from self.g
		g = Graph() + self.g
		data_ns = self.data_ns
		d = data_ns[parameter_id + '_data']
		g.add((d, RDF.type, data_ns.VectorData))
		g.add((d, DCTERMS.identifier, Literal(re.sub('^para_', '', parameter_id))))
		g.add((d, data_ns.dataContent, Literal(metadata['content'])))
		g.add((d, data_ns.dataFormat, data_ns[Utils.normalize(metadata['format'])]))
		g.add((d, data_ns.hasCRSProj4, Literal(metadata['proj4'])))
		g.add((d, data_ns.hasCRSWkt, Literal(metadata['wkt'])))
		if self._get_uom(metadata['uom']) is not None:
			g.add((d, data_ns.hasUOM, self._get_uom(metadata['uom'])))
		g.add((d, data_ns.dataTheme, Literal(data_theme)))
		g.add((d, data_ns.isProjected, Literal(True if metadata['isProjected'] > 0 else False, datatype=XSD.boolean)))
		if metadata['epsg'] is not None:
			g.add((d, data_ns.hasEPSG, Literal('EPSG:' + metadata['epsg'])))
		if metadata['isProjected'] > 0:
			g.add((d, data_ns.hasCRS, Literal(metadata['projcs'])))
		else:
			g.add((d, data_ns.hasCRS, Literal(metadata['geogcs'])))
		g.add((d, self.geo.hasGeometry, self.sf[metadata['geometry']]))
		ddtype = XSD.double
		g.add((d, data_ns.centralX, Literal(self._format(metadata['centroid'][0]), datatype=ddtype)))
		g.add((d, data_ns.centralY, Literal(self._format(metadata['centroid'][1]), datatype=ddtype)))
		g = self._add_extent(g, d, metadata['extent'][0], metadata['extent'][2], metadata['extent'][1], metadata['extent'][3])
		return g

	def raster_graph(self, parameter_id, data, data_theme=None):
		"""
		translate raster metadata into RDF graph
		Args:
			parameter_id: parameter identifier
			data: input data
			data_theme: data theme of input data

		Returns:
			graph

		"""
		data_ns = self.data_ns
		metadata = GeoMetadata.raster_metadata(data, data_theme)
		g = Graph() + self.g
		d = data_ns[parameter_id + '_data']
		g.add((d, RDF.type, data_ns.RasterData))
		g.add((d, DCTERMS.identifier, Literal(re.sub('^para_', '', parameter_id))))
		g.add((d, data_ns.dataContent, Literal(metadata['content'])))
		g.add((d, data_ns.dataFormat, data_ns[Utils.normalize(metadata['format'])]))
		g.add((d, data_ns.bandCount, Literal(metadata['band_count'])))
		ddtype = XSD.double
		g.add((d, data_ns.bandMinValue, Literal(self._format(metadata['min']), datatype=ddtype)))
		g.add((d, data_ns.bandMaxValue, Literal(self._format(metadata['max']), datatype=ddtype)))
		g.add((d, data_ns.bandMeanValue, Literal(self._format(metadata['mean']), datatype=ddtype)))
		g.add((d, data_ns.bandStdDev, Literal(self._format(metadata['stddev']), datatype=ddtype)))
		dtype = XSD[type(metadata['nodata']).__name__]
		g.add((d, data_ns.nodataValue, Literal(metadata['nodata'], datatype=dtype)))
		g.add((d, data_ns.hasCRSProj4, Literal(metadata['proj4'])))
		g.add((d, data_ns.hasCRSWkt, Literal(metadata['wkt'])))
		g.add((d, data_ns.dataTheme, Literal(data_theme)))
		if self._get_uom(metadata['uom']) is not None:
			g.add((d, data_ns.hasUOM, self._get_uom(metadata['uom'])))
		g.add((d, data_ns.isProjected, Literal(True if metadata['isProjected'] > 0 else False, datatype=XSD.boolean)))
		if metadata['epsg'] is not None:
			g.add((d, data_ns.hasEPSG, Literal('EPSG:' + metadata['epsg'])))
		if metadata['isProjected'] > 0:
			if metadata['projcs']:
				g.add((d, data_ns.hasCRS, Literal(metadata['projcs'])))
			if metadata['geogcs']:
				g.add((d, data_ns.hasCRS, Literal(metadata['geogcs'])))
		g.add((d, data_ns.centralX, Literal(self._format(metadata['centroid'][0]), datatype=ddtype)))
		g.add((d, data_ns.centralY, Literal(self._format(metadata['centroid'][1]), datatype=ddtype)))
		g = self._add_extent(g, d, metadata['extent'][0], metadata['extent'][1], metadata['extent'][2], metadata['extent'][3])
		dtype = XSD[type(metadata['resolution']).__name__]
		g.add((d, data_ns.spatialResolution, Literal(metadata['resolution'], datatype=dtype)))
		return g

	def general_graph(self, parameter_id, data, data_theme=None):
		"""
		translate general data (non-geospatial data) into RDF graph
		Args:
			parameter_id: parameter identifier
			data: input data
			data_theme: data theme of input data

		Returns:
			graph

		"""
		g = Graph() + self.g
		d = self.data_ns[parameter_id + '_data']
		g.add((d, RDF.type, self.data_ns.LiteralData))
		g.add((d, DCTERMS.identifier, Literal(re.sub('^para_', '', parameter_id))))
		if os.path.isfile(data) or os.path.isdir(data):
			data = os.path.basename(data)
		g.add((d, self.data_ns.dataContent, Literal(data, datatype=XSD[type(data)])))
		g.add((d, self.data_ns.dataTheme, Literal(data_theme)))
		return g
