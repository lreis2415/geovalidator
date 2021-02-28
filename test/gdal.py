
from osgeo import gdal, ogr, osr


def version():
    print(gdal.VersionInfo())

def shp():
    data =  '../data/Heihe_Meteorology_Station_Distribution.shp'
    ds = ogr.Open(data)
    if ds is None:
        raise ValueError('Invalid vector data')
    print(ds.GetDriver().name)

if __name__ == '__main__':
    shp()