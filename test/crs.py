import pycrs

crs = pycrs.load.from_url("http://spatialreference.org/ref/esri/54030/ogcwkt/")

proj4 = "+proj=tmerc +lat_0=0 +lon_0=117 +k=1 +x_0=39500000 +y_0=0 +ellps=krass +units=m +no_defs"
crs2 = pycrs.parse.from_proj4(proj4)
print(crs2.name)
print(crs2.to_ogc_wkt())

crs3 = pycrs.parse.from_epsg_code(2415)

print(crs3.name)
print(crs3.to_ogc_wkt())



from osgeo import osr
# WGS84 projection reference
OSR_WGS84_REF = osr.SpatialReference()
OSR_WGS84_REF.ImportFromEPSG(4326)
# original
OSR_o = osr.SpatialReference()
epsg = 2415
OSR_o.ImportFromEPSG(epsg)

to_wgs84 = osr.CoordinateTransformation(OSR_o,OSR_WGS84_REF)

# minx, miny,z = to_wgs84.TransformPoint(minx, miny)
# maxx, maxy,z = to_wgs84.TransformPoint(maxx, maxy)