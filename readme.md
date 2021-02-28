# GeoValidator
>beta 0.1 
>by *hou-zhi-wei @ lreis, igsnrr, CAS*

Translate input (geospatial/non-geospatial) data of a geoprocessing tool parameter into RDF graphs and validate it against predefined [SHACL](https://www.w3.org/TR/shacl) shape graph.

checks the
- completeness
- correctness
- consistency

all shapes graphs shown in the article are listed in directory `shapes`

based on 
- [pySHACL](https://github.com/RDFLib/pySHACL)
   > `conda install -c conda-forge pyshacl `
- [GDAL](https://gdal.org/index.html)
- [RDFLib](https://github.com/RDFLib/rdflib)


---
Hands on:
1. define SHACL shapes graphs. can be coded manually or generated with codes based on rdflib. see generator/list*.py
2. translate input data to data graph, see generator/to_graphs.py
3. link functionality to its inputs in data graph
4. validate input data, as shown in `test/test_validator.py`
5. validation reports: `test/case*_report.ttl`

Note:
for validation report part:
```turtle
sh:value [ a geo:Geometry,
             geo:SpatialObject,
             sf:Geometry,
             sf:Point,
             rdfs:Resource ]
```
the value is an instance of `sf:Point`, thus it is also an instance of `sf:Geometry` and other classes .
(`sf:Geometry` is a subclass of `geo:Geometry`)

---
[SHACL Playground](https://shacl.org/playground/) is perfect for testing constraints defined using built-in SHACL Core Constraint Components

---
References:
- [SHACL](https://www.w3.org/TR/shacl)
- [SHACL Advanced Features](https://www.w3.org/TR/shacl-af)
- [Validating RDF Data](http://book.validatingrdf.com/)