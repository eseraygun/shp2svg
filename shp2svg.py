import sys
import codecs
import pyproj
import shapefile

input = codecs.getreader("utf-8")(sys.stdin)
output = codecs.getwriter("utf-8")(sys.stdout)

if len(sys.argv) != 3:
    print >> sys.stderr, "USAGE %s projection shapefile" % sys.argv[0]
    sys.exit(1)
projectionName = sys.argv[1]
shapefileName = sys.argv[2]

class Polygon(object):
    def __init__(self):
        self.id = u""
        self.coords = list()
        self.pcoords = list()
        self.ncoords = list()

# Read shapefile
polygons = list()
reader = shapefile.Reader(shapefileName)
shapes = reader.shapes()
shapeIndex = 0
for shape in shapes:
    parts = list(shape.parts) + [len(shape.points)]
    for partIndex in xrange(0, len(parts) - 1):
        points = shape.points[parts[partIndex]:parts[partIndex + 1]]
        polygon = Polygon()
        polygon.id = "shape_%03d_%03d" % (shapeIndex, partIndex)
        polygon.coords = list()
        for point in points:
            lon, lat = point[0], point[1]
            if lat > 89.0:
                lat = 89.0
            elif lat < -89.0:
                lat = -89.0
            polygon.coords.append((lon, lat))
        polygons.append(polygon)
    shapeIndex += 1

#for polygon in polygons:
#    print >> sys.stderr, "INFO", "raw %s" % polygon.id
#    print >> sys.stderr, "INFO", "  %s" % \
#            u" ".join(map(lambda coord: "%4.2f,%4.2f" % coord, polygon.coords))

# Determine limits
minLon = None
minLat = None
maxLon = None
maxLat = None
for polygon in polygons:
    for coord in polygon.coords:
        lon, lat = coord[0], coord[1]
        if minLon == None or lon < minLon: minLon = lon
        if minLat == None or lat < minLat: minLat = lat
        if maxLon == None or lon > maxLon: maxLon = lon
        if maxLat == None or lat > maxLat: maxLat = lat
avgLon = (minLon + maxLon) * 0.5
avgLat = (minLat + maxLat) * 0.5

# Project coordinates
proj = pyproj.Proj(proj=projectionName) #, lon_0=avgLon, lat_ts=avgLat)
minX = None
minY = None
maxX = None
maxY = None
for polygon in polygons:
    polygon.pcoords = list()
    for coord in polygon.coords:
        x, y = proj(coord[0], coord[1])
        polygon.pcoords.append((x, y))
        if minX == None or x < minX: minX = x
        if minY == None or y < minY: minY = y
        if maxX == None or x > maxX: maxX = x
        if maxY == None or y > maxY: maxY = y
dx = maxX - minX
dy = maxY - minY
d = max(dx, dy)
s = 1024.0 / d
print >> sys.stderr, "INFO", "minX:%s minY:%s maxX:%s maxY:%s s:%s" % (minX, minY, maxX, maxY, s)

#for polygon in polygons:
#    print >> sys.stderr, "INFO", "projected %s" % polygon.id
#    print >> sys.stderr, "INFO", "  %s" % \
#            u" ".join(map(lambda coord: "%4.2f,%4.2f" % coord, polygon.pcoords))

# Normalize coordinates
for polygon in polygons:
    polygon.ncoords = list()
    for pcoord in polygon.pcoords:
        x = (pcoord[0] - minX) * s
        y = (maxY - pcoord[1]) * s
        polygon.ncoords.append((int(x), int(y)))
w = int(dx * s)
h = int(dy * s)

#index = 0
#for polygon in polygons:
#    print >> sys.stderr, "INFO", "normalized %s" % polygon.id
#    print >> sys.stderr, "INFO", "  %s" % \
#            u" ".join(map(lambda coord: "%4.2f,%4.2f" % coord, polygon.ncoords))
#    index += 1
#    if index == 3:
#        break

output.write(u'<?xml version="1.0" standalone="no"?>'
        '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
        '<svg width="%d" height="%d" version="1.1" xmlns="http://www.w3.org/2000/svg">' % (w, h))
for polygon in polygons:
    output.write(u"<polygon id=\"disctrict%s\" points=\"" % polygon.id)
    output.write(u" ".join(map(lambda ncoord: "%d,%d" % ncoord, polygon.ncoords)))
    output.write(u"\" style=\"fill:#cccccc; stroke:#000000;stroke-width:1\" />\n")
output.write("</svg>\n")

