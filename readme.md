# GeoValidator
>beta 0.1 
>by *hou-zhi-wei @ lreis, igsnrr, CAS*

Translate input (geospatial/non-geospatial) data of a geoprocessing functionality parameter into RDF graphs and validate it against predefined [SHACL](https://www.w3.org/TR/shacl) shape graph.

checks the
- completeness
- correctness
- consistency

based on 
- [pySHACL](https://github.com/RDFLib/pySHACL)
- [GDAL](https://gdal.org/index.html)
- [RDFLib](https://github.com/RDFLib/rdflib)


[SHACL Playground](https://shacl.org/playground/) is perfect for testing constraints defined using built-in SHACL Core Constraint Components

---
References:
- [SHACL](https://www.w3.org/TR/shacl)
- [SHACL Advanced Features](https://www.w3.org/TR/shacl-af)
- [Validating RDF Data](http://book.validatingrdf.com/)