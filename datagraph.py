#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2020/1/5 18:01

import os
import re
from rdflib import Graph, RDF, Literal, XSD, BNode, URIRef
from rdflib.namespace import DCTERMS, SKOS,DCAT
from metadata import GeoMetadata
from utils import Utils, DATA, GEO, SF, PROCESS, SH, UNIT, SOFT


class DataGraph(object):
    def __init__(self):
        """
        namespaces and bind prefixes
        """
        self.g = Graph()
        self.g.bind('data', DATA)
        self.g.bind('process', PROCESS)
        self.g.bind('soft', SOFT)
        self.g.bind('sh', SH)
        self.g.bind('geo', GEO)
        self.g.bind('sf', SF)
        self.g.bind('skos', SKOS)
        self.g.bind('dcat', DCAT)
        self.g.bind('vocab', 'http://www.egc.org/ont/vocab#')
        self.g.bind('unit', UNIT)
        self.g.bind('dcterms', DCTERMS)
        self.g.bind('gemet', 'https://www.eionet.europa.eu/gemet/concept/')
        self.g.bind('gcmd', 'https://gcmdservices.gsfc.nasa.gov/kms/concept/')
        self.g.bind('theme', 'http://inspire.ec.europa.eu/theme/')
        self.g.bind('locn', 'http://www.w3.org/ns/locn#')

        self.gemet_dem = URIRef('https://www.eionet.europa.eu/gemet/concept/10140')
        self.vocab_dem = URIRef('http://www.egc.org/ont/vocab#DEM')
        self.gcmd_dem = URIRef('https://gcmdservices.gsfc.nasa.gov/kms/concept/digital_elevation_models')
        self.theme_dem = URIRef('http://inspire.ec.europa.eu/theme/el')
        self.gemet_soil = URIRef('https://www.eionet.europa.eu/gemet/concept/7843')
        self.gcmd_soil = URIRef('https://gcmdservices.gsfc.nasa.gov/kms/concept/soils')
        self.theme_soil = URIRef('http://inspire.ec.europa.eu/theme/so')
        self.gemet_landuse = URIRef('https://www.eionet.europa.eu/gemet/concept/4678')
        self.gemet_landcover = URIRef('https://www.eionet.europa.eu/gemet/concept/4612')
        self.gcmd_landuse = URIRef('https://gcmdservices.gsfc.nasa.gov/kms/concept/land_use')
        self.gcmd_landcover = URIRef('https://gcmdservices.gsfc.nasa.gov/kms/concept/land_cover')
        self.theme_landuse = URIRef('http://inspire.ec.europa.eu/theme/lu')
        self.theme_landcover = URIRef('http://inspire.ec.europa.eu/theme/lc')


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
        file_dir = os.path.dirname(file_path)
        if os.path.isdir(file_dir) and not os.path.exists(file_dir):
            # if not os.path.exists(os.path.dirname(file_path)):
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
            return UNIT.DEG
        elif meta_uom == 'meter' or meta_uom == 'metre':
            return UNIT.M
        else:
            unit_g = Graph()
            unit_g.parse("../ont/QUDT ALL UNITS.ttl", format="turtle")
            for uom in unit_g.subjects(SKOS.prefLabel, Literal(meta_uom)):
                return uom


    def set_theme(self,graph,node,theme):
        if(theme == 'DEM'):
            graph.add((node, DCAT.theme, self.theme_dem))
            graph.add((node, DCAT.theme, self.gcmd_dem))
            graph.add((node, DCAT.theme, self.gemet_dem))
            graph.add((node, DCAT.theme, self.vocab_dem))
            graph.add((node, DCTERMS.subject, self.vocab_dem))
        elif(theme=='Landuse'):
            graph.add((node, DCAT.theme, self.theme_landuse))
            graph.add((node, DCAT.theme, self.gcmd_landuse))
            graph.add((node, DCAT.theme, self.gemet_landuse))
        elif(theme=='Landcover'):
            graph.add((node, DCAT.theme, self.gcmd_landcover))
            graph.add((node, DCAT.theme, self.gemet_landcover))
            graph.add((node, DCAT.theme, self.theme_landcover))
        elif(theme=='Soil'):
            graph.add((node, DCAT.theme, self.theme_soil))
            graph.add((node, DCAT.theme, self.gcmd_soil))
            graph.add((node, DCAT.theme, self.gemet_soil))
        else:
            theme_node = URIRef('http://www.egc.org/ont/vocab#' + theme)
            graph.add((theme_node, SKOS.prefLabel, Literal(theme)))
            graph.add((theme_node, DCTERMS.type, SKOS.Concept))
            graph.add((node, DCAT.theme, theme_node))

    def set_crs(self, graph, node, crsStr):
        import re
        # data_g = Graph()
        # data_g.parse("../ont/data.owl", format="xml")
        srs = URIRef('http://inspire.ec.europa.eu/glossary/SpatialReferenceSystem')
        crs = URIRef('http://www.egc.org/ont/data#CoordinateReferenceSystem')
        n = URIRef('http://www.egc.org/ont/data#' + crsStr)

        file = '../ont/esri_epsg.wkt'
        epsg= None
        with open(file) as f:
            for cnt, line in enumerate(f):
                if line[0] == '#' or line[0] == '\n':
                    continue
                else:
                    temp = line.split(',', 1)
                    wkt = temp[1]
                    crs_name = re.match(r"(PROJCS|GEOGCS)[\"[0-9a-zA-Z_(.+/)-]+(?=\")", wkt)
                    name = re.sub(r'(PROJCS|GEOGCS)\[\"', '', crs_name.group())
                    if name == crsStr:
                        epsg = temp[0]


        graph.add((n, RDF.type, srs))
        graph.add((n, RDF.type, crs))
        graph.add((n, DATA.hasEPSG, Literal(epsg,datatype=XSD.int)))
        graph.add((n, SKOS.prefLabel, Literal(crsStr)))
        graph.add((node, DATA.hasCRS, n))
        graph.add((node, DATA.hasEPSG, Literal(epsg,datatype=XSD.int)))
        graph.add((node, DATA.hasSRID, Literal("EPSG:"+epsg)))
        return epsg
        # data_g.add((n, SKOS.altLabel, Literal(crsStr)))
        # crs_node = None
        # for c in data_g.subjects(SKOS.prefLabel, Literal(crsStr)):
        #     if c is not None:
        #         crs_node =  c
        #         break
        # if crs_node is not None:
        #     return crs_node
        # else:
        #     n = URIRef('http://www.egc.org/ont/data#' + crsStr)
        #     data_g.add((n, RDF.type, srs))
        #     data_g.add((n, RDF.type, crs))
        #     data_g.add((n, SKOS.prefLabel, Literal(crsStr)))
            # data_g.add((n, SKOS.altLabel, Literal(crsStr)))
            # if epsg:
            #     data_g.add((n, DATA.hasEPSG, Literal(epsg)))
                # will be changed to RDF file
                # data_g.serialize("../ont/data.owl", format="xml")
                # data_g.serialize("../ont/data.ttl", format="turtle")
            # return n

    def _add_extent(self, g, node, minx, miny, maxx, maxy,epsg:int):
        minx0 = self._format(minx)
        miny0 = self._format(miny)
        maxx0 = self._format(maxx)
        maxy0 = self._format(maxy)
        # dtype = XSD.double
        # g.add((node, DATA.minX, Literal(minx, datatype=dtype)))
        # g.add((node, DATA.westBoundingCoordinate, Literal(minx, datatype=dtype)))
        # g.add((node, DATA.maxX, Literal(maxx, datatype=dtype)))
        # g.add((node, DATA.eastBoundingCoordinate, Literal(maxx, datatype=dtype)))
        # g.add((node, DATA.minY, Literal(miny, datatype=dtype)))
        # g.add((node, DATA.southBoundingCoordinate, Literal(miny, datatype=dtype)))
        # g.add((node, DATA.maxY, Literal(maxy, datatype=dtype)))
        # g.add((node, DATA.northBoundingCoordinate, Literal(maxy, datatype=dtype)))
        # g.add((node, DATA.spatialExtent, Literal(str(minx) + ',' +
        #                                          str(miny) + ',' + str(maxx) + ',' + str(maxy), datatype=XSD.string)))
        if epsg != 4326:
            from osgeo import osr
            # WGS84 projection reference
            OSR_WGS84_REF = osr.SpatialReference()
            OSR_WGS84_REF.ImportFromEPSG(4326)
            # original
            OSR_o = osr.SpatialReference()
            # must use int(epsg) otherwise case error
            OSR_o.ImportFromEPSG(int(epsg))

            to_wgs84 = osr.CoordinateTransformation(OSR_o,OSR_WGS84_REF)

            minx, miny,z = to_wgs84.TransformPoint(float(minx0), float(miny0))
            maxx, maxy,z1 = to_wgs84.TransformPoint(float(maxx0), float(maxy0))

        locn_geometry=URIRef('http://www.w3.org/ns/locn#geometry')
        gsp_wktLiteral=URIRef('http://www.opengis.net/ont/geosparql#wktLiteral')
        loc = BNode()
        g.add((loc,RDF.type,DCTERMS.Location))
        g.add((loc,locn_geometry,Literal('POLYGON(('+str(minx) + ' ' + str(miny) + ','
                                         +str(minx) + ' ' + str(maxy) + ','
                                         +str(maxx) + ' ' + str(maxy) + ','
                                         +str(maxx) + ' ' + str(miny) + ','
                                         +str(minx) + ' ' + str(miny) +'))',datatype=gsp_wktLiteral)))
        g.add((node,DCTERMS.spatial,loc))
        return g

    def vector_graph(self, tool_ontology, parameter_id, data, data_theme=None): 
        """
        translate vector metadata into RDF graph
        Args:
                tool_ontology: tool ontology, e.g., ArcGIS in utils.py
				parameter_id: parameter identifier
                data: input data
                data_theme: data theme of input data

        Returns:
                graph

        """
        metadata = GeoMetadata.vector_metadata(data, data_theme)
        # a new graph with everything from self.g
        g = Graph() + self.g
        d = BNode()
        g.add((d, RDF.type, DATA.VectorData))
        g.add((d, DATA.parameterId, Literal(parameter_id)))
        g.add((d, DATA.dataContent, Literal(metadata['content'])))
        g.add((d, DATA.dataFormat, DATA[Utils.normalize(metadata['format'])]))
        g.add((d, DATA.hasCRSProj4, Literal(metadata['proj4'])))
        g.add((d, DATA.hasCRSWkt, Literal(metadata['wkt'])))
        if self._get_uom(metadata['uom']) is not None:
            g.add((d, DATA.hasUOM, self._get_uom(metadata['uom'])))

        self.set_theme(g,d,data_theme)
        # g.add((d, DCAT.theme, Literal(data_theme)))

        g.add((d, DATA.isProjected, Literal(
            True if metadata['isProjected'] > 0 else False, datatype=XSD.boolean)))
        # if metadata['epsg'] is not None:
        #     g.add((d, DATA.hasEPSG, Literal('EPSG:' + metadata['epsg'])))
        epsg = metadata['epsg']
        if metadata['isProjected'] > 0:
            epsg =  self.set_crs(g, d, metadata['projcs'])
        else:
            epsg =  self.set_crs(g, d, metadata['geogcs'])

        # gb = BNode()
        # g.add((gb, RDF.type, SF[metadata['geometry']]))
        g.add((d, DCTERMS.type, SF[metadata['geometry']]))
        # g.add((d, GEO.hasGeometry, gb))

        ddtype = XSD.double
        # g.add((d, DATA.centralX, Literal(self._format(
        #     metadata['centroid'][0]), datatype=ddtype)))
        # g.add((d, DATA.centralY, Literal(self._format(
        #     metadata['centroid'][1]), datatype=ddtype)))
        g = self._add_extent(
             g, d, metadata['extent'][0], metadata['extent'][2], metadata['extent'][1], metadata['extent'][3],epsg)

        t_parameter = tool_ontology[parameter_id.replace(' ','_')]
        g.add((t_parameter, DCTERMS.identifier, Literal(parameter_id)))
        g.add((t_parameter, PROCESS['hasData'], d))

        return g

    def raster_graph(self, tool_ontology, parameter_id, data, data_theme=None):
        """
        translate raster metadata into RDF graph
        Args:
                tool_ontology: tool ontology, e.g., arcgis
                parameter_id: parameter identifier
                data: input data
                data_theme: data theme of input data

        Returns:
                graph

        """
        metadata = GeoMetadata.raster_metadata(data, data_theme)
        g = Graph() + self.g
        d = BNode()
        g.add((d, RDF.type, DATA.RasterData))
        g.add((d, DATA.parameterId, Literal(parameter_id)))
        g.add((d, DATA.dataContent, Literal(metadata['content'])))
        g.add((d, DATA.dataFormat, DATA[Utils.normalize(metadata['format'])]))
        # g.add((d, DATA.bandCount, Literal(metadata['band_count'])))
        # ddtype = XSD.double
        # g.add((d, DATA.bandMinValue, Literal(
        #     self._format(metadata['min']), datatype=ddtype)))
        # g.add((d, DATA.bandMaxValue, Literal(
        #     self._format(metadata['max']), datatype=ddtype)))
        # g.add((d, DATA.bandMeanValue, Literal(
        #     self._format(metadata['mean']), datatype=ddtype)))
        # g.add((d, DATA.bandStdDev, Literal(
        #     self._format(metadata['stddev']), datatype=ddtype)))
        dtype = XSD[type(metadata['nodata']).__name__]
        g.add((d, DATA.nodataValue, Literal(
            metadata['nodata'], datatype=dtype)))
        g.add((d, DATA.hasCRSProj4, Literal(metadata['proj4'])))
        g.add((d, DATA.hasCRSWkt, Literal(metadata['wkt'])))
        self.set_theme(g,d,data_theme)
        # g.add((d, DATA.dataTheme, Literal(data_theme)))
        if self._get_uom(metadata['uom']) is not None:
            g.add((d, DATA.hasUOM, self._get_uom(metadata['uom'])))
        g.add((d, DATA.isProjected, Literal(
            True if metadata['isProjected'] > 0 else False, datatype=XSD.boolean)))
        # epsg code may be wrong
        # if metadata['epsg'] is not None:
        #     g.add((d, DATA.hasEPSG, Literal('EPSG:' + metadata['epsg'])))
        epsg = metadata['epsg']
        if metadata['isProjected'] > 0:
            g.add((d, DATA.srsName, Literal(metadata['projcs'])))
            epsg = self.set_crs(g, d, metadata['projcs'])
        else:
            g.add((d, DATA.srsName, Literal(metadata['geogcs'])))
            epsg = self.set_crs(g, d, metadata['geogcs'])

        # g.add((d, DATA.centralX, Literal(self._format(
        #     metadata['centroid'][0]), datatype=ddtype)))
        # g.add((d, DATA.centralY, Literal(self._format(
        #     metadata['centroid'][1]), datatype=ddtype)))
        g = self._add_extent(
            g, d, metadata['extent'][0], metadata['extent'][1], metadata['extent'][2], metadata['extent'][3],epsg)
        #dtype = XSD[type(metadata['resolution']).__name__]
        g.add((d, DCAT.spatialResolutionInMeters, Literal(
            metadata['resolution'], datatype=XSD.decimal)))

        t_parameter = tool_ontology[parameter_id.replace(' ','_')]
        g.add((t_parameter, DCTERMS.identifier, Literal(parameter_id)))
        g.add((t_parameter, PROCESS['hasData'], d))

        return g

    def general_graph(self, tool_ontology, parameter_id, data, data_theme=None):
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
        d = BNode()
        g.add((d, RDF.type, DATA.LiteralData))
        g.add((d, DATA.parameterId, Literal( parameter_id.replace('_',' '))))
        if os.path.isfile(data) or os.path.isdir(data):
            data = os.path.basename(data)
        g.add((d, DATA.dataContent, Literal(data, datatype=XSD[type(data)])))
        g.add((d, DATA.dataTheme, Literal(data_theme)))

        t_parameter = tool_ontology[parameter_id]
        g.add((t_parameter, DCTERMS.identifier, Literal(parameter_id.replace('_',' '))))
        g.add((t_parameter, PROCESS['hasData'], d))

        return g

    def parameter_value_graph(self, tool_ontology, parameter_id, data):
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
        d = BNode()
        g.add((d, RDF.type, DATA.LiteralData))
        g.add((d, DCTERMS.identifier, Literal(parameter_id)))
        g.add((d, DATA.parameterId, Literal( parameter_id)))
        if os.path.isfile(data) or os.path.isdir(data):
            data = os.path.basename(data)
        g.add((d, DATA.dataContent, Literal(data, datatype=XSD[type(data)])))

        t_parameter = tool_ontology[parameter_id]
        g.add((t_parameter, PROCESS['hasLiteralData'], Literal(data, datatype=XSD[type(data)])))

        return g
    # def functionality_data_graph(self, tool_uri: URIRef, *input_data_graph: Graph):
    #     """
    #     construct a tool level data graph
    #     :param tool_uri: e.g., arcgis:clip_analysis
    #     :param input_data_graph:
    #     :return:
    #     """
    #     graph = Graph()
    #     for in_graph in input_data_graph:
    #         # a generator
    #         in_data = in_graph.subjects(RDF.type, None)
    #         graph.add((tool_uri, PROCESS.hasInputData, next(in_data)))
    #     return graph
