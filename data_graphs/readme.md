in order to test data without CRS, comment the following lines in L7_clip_line_no_epsg.ttl
```
    # data:hasCRS "CGCS2000 / 3-degree Gauss-Kruger zone 40" ;
    # data:hasCRSProj4 "+proj=tmerc +lat_0=0 +lon_0=120 +k=1 +x_0=40500000 +y_0=0 +ellps=GRS80 +units=m +no_defs " ;
    # data:hasCRSWkt "PROJCS[\"CGCS2000 / 3-degree Gauss-Kruger zone 40\",GEOGCS[\"China Geodetic Coordinate System 2000\",DATUM[\"China_2000\",SPHEROID[\"CGCS2000\",6378137,298.257222101,AUTHORITY[\"EPSG\",\"1024\"]],AUTHORITY[\"EPSG\",\"1043\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AUTHORITY[\"EPSG\",\"4490\"]],PROJECTION[\"Transverse_Mercator\"],PARAMETER[\"latitude_of_origin\",0],PARAMETER[\"central_meridian\",120],PARAMETER[\"scale_factor\",1],PARAMETER[\"false_easting\",40500000],PARAMETER[\"false_northing\",0],UNIT[\"metre\",1,AUTHORITY[\"EPSG\",\"9001\"]],AUTHORITY[\"EPSG\",\"4528\"]]" ;
    # data:hasEPSG "EPSG:4528" ;
```

L7_all.ttl merges L7_clip_line.ttl and L7_input_polygon.ttl