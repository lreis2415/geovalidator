import re

file = '../ont/esri_epsg.wkt'

with open(file) as f:
   for cnt, line in enumerate(f):
       if line[0]=='#' or line[0]=='\n':
           continue
       else:
          temp = line.split(',',1)

          epsg = temp[0]
          wkt = temp[1]
          crs_name = re.match(r"(PROJCS|GEOGCS)[\"[0-9a-zA-Z_(.+/)-]+(?=\")",wkt)
          name = re.sub(r'(PROJCS|GEOGCS)\[\"','',crs_name.group())
          print(name)
          if name is None or name=='GEOGCS[' or name=='PROJCS[':
              print(temp)
       # print("Line {}: {}".format(cnt, line))
