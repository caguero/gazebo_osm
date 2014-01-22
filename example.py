#!/usr/bin/env python
from dict2sdf import GetSDF
from osm2dict import Osm2Dict


osmRoads = Osm2Dict()
roadPointWidthMap = osmRoads.getRoadCoords()

sdfFile = GetSDF()
sdfFile.addModule("sun")
sdfFile.addModule("ground_plane")
sdfFile.addSphericalCoords(osmRoads.getLat(), osmRoads.getLon())

for road in roadPointWidthMap.keys():
  
  sdfFile.addRoad( road )

  sdfFile.setRoadWidth( roadPointWidthMap[road]['width'], road)
  
  points = roadPointWidthMap[ road]['points']
  for point in range(len(points[0,:])):
    sdfFile.addRoadPoint([points[0,point], points[1,point], points[2,point]], road)
   
sdfFile.writeToFile('outFile2.sdf')
 
