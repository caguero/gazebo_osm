#!/usr/bin/env python
import osmapi
import numpy as np
from dict2sdf import GetSDF

class Osm2Dict:
  #Radius of the Earth in km
  def __init__(self):
    self.R = 6371
    self.records = dict()
    
           #highway values for roads
   
    self.highwayWidthRelation= dict({ "motorway": 4, "trunk" : 3  , "primary" : 1.5, "secondary": 0.8 , "tertiary" : 0.42, "residential": 0.21})
  
   #highwayRoadValues= [ "primary", "motorway", "motorway_link", "trunk", "trunk_link", "primary", "primary_link","secondary", "secondary_link", "tertiary", "tertiary_link", "living_street", "pedestrian","resedential", "unclassified", "service", "bus_guideway", "raceway", "road"]

    #get map coords
    print("\nPlease enter the latitudnal and logitudnal coordinates of the area or select from default by hitting return twice \n")
    startCoords = raw_input("Enter starting coordinates: [lon lat] :").split(' ') 
    endCoords = raw_input("Enter ending coordnates: [lon lat]: ").split(' ')
  
    if startCoords != [] and endCoords != [] and len(startCoords) == 2 and len(endCoords) == 2:
      for incoords in range(2):
        startCoords[incoords] = float(startCoords[incoords])
        endCoords[ incoords ] = float(endCoords[incoords])
    else:
      choice = raw_input("Default Coordinate options: West El Camino Highway, CA (default), Bethlehem, PA (2): ")
      if choice == '2':
        startCoords, endCoords = [ 40.6103478, -75.3826048], [ 40.6087963, -75.3718421]
      else:
        startCoords, endCoords = [37.385844 , -122.101464 ],[37.395664 , -122.083697]

    self.latStart = startCoords[0]
    self.lonStart = startCoords[1]
    self.latStop = endCoords[0]
    self.lonStop = endCoords[1]	
 

  def latLonDist(self, coords ):
    distance = np.array([])
    for cordinate in range(len(coords)):
      lon2 = np.radians(coords[cordinate,0])
      lat2 = np.radians(coords[cordinate, 1])
   
      dLat = (lat2-np.radians(self.latStart));
      dLon = (lon2-np.radians(self.lonStart));
  
      a = np.sin(dLat/2) * np.sin(dLat/2) + np.sin(dLon/2) * np.sin(dLon/2) * np.cos(np.radians(self.latStart)) * np.cos(lat2); 
      c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a)); 
      distance = np.append(distance, self.R * c) 
    return distance
  
  
  def latLongBearing(self, coords):
    angle = np.array([])
    for i in range(len(coords)):
      lon2 = np.radians(coords[i][0])
      lat2 = np.radians(coords[i][ 1])
  
      dLat = (lat2-np.radians(self.latStart));
      dLon = (lon2-np.radians(self.lonStart));
      angle = np.append(angle, np.arctan2( np.sin(dLon) * np.cos(lat2), np.cos(np.radians(self.latStart)) * np.sin(lat2) - np.sin(np.radians(self.latStart)) * np.cos(lat2) * np.cos(dLon)))
    return angle
  
  def getPoints( self, coords ):
    distance = self.latLonDist( coords )
    angles = self.latLongBearing( coords)
   
    point = np.array([ distance*np.cos(angles), distance*np.sin(angles), np.zeros(np.shape(distance))])
    return point
   
  def getRoadCoords(self):
   
   #initialize the Open street api
    MyApi = osmapi.OsmApi()
    
    #Get the map data reqd
    data = MyApi.Map( min(self.lonStart, self.lonStop), min(self.latStart, self.latStop), max(self.lonStart, self.lonStop), max(self.latStart, self.latStop))
   
    # get the road latitude and longitudes
    for i in range( len(data) ):
      if "way" in data[i].get("type"):
      
        if "highway" in data[i].get("data").get("tag"):
        
          highwayType = data[i].get("data").get("tag").get("highway")
          
          if highwayType in self.highwayWidthRelation.keys():
          
                roadName = data[i].get("data").get("tag").get("name") 
                if roadName == None: 
		     roadName = highwayType + "_" +  str(data[i].get("data").get("id"))

                else:
                     roadName += "_" +  str(data[i].get("data").get("id"))

		
                node_ref = data[i].get("data").get("nd")
                coords = np.array([])
                for j in range( len(data) ):
                  if "node" in data[j].get("type")  :
    
                     if data[j].get("data").get("id") in node_ref: 
                      coords = np.append(coords, data[j].get("data").get("lon"))
                      coords = np.append( coords, data[j].get("data").get("lat"))          
                      coords = np.reshape(coords,(len(coords)/2, 2))
                      			                 
                pointsXYZ = self.getPoints(coords)
                 #Sort points in X, Y, Z 
                index = np.lexsort((pointsXYZ[0,:], pointsXYZ[1,:], pointsXYZ[2,:]))
                orderedPoints = pointsXYZ[:,index]
                self.records.update(dict({roadName : { 'points' : orderedPoints, 'width': self.highwayWidthRelation[ highwayType ] }}))
    return self.records          

  def getLat(self):
      return self.latStart

  def getLon(self):
      return self.lonStart

