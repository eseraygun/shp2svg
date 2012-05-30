shp2svg
=======

Shapefile to SVG conversion with arbitrary projection.

# Usage

`shp2svg.py projection shapefile`

* projection – name of the projection. For example, `aea` stands for Albers Equal-Area Conic projection. For a list of supported projections see [here](http://www.remotesensing.org/geotiff/proj_list).
* shapefile – path to the shapefile

# Dependencies

shp2svg depends on the following Python libraries.

* [shapefile](http://code.google.com/p/pyshp/) – for parsing
* [pyproj](http://code.google.com/p/pyproj/) – for projections

# Missing Features

* Passing parameters to the projection through the command-line interface.
* Customizing SVG generation (eg. colors and ids).
