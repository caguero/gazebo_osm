import elementtree.ElementTree as Et
import xml.dom.minidom as minidom



class GetSDF:

	def __init__(self):	
		self.sdf = Et.Element('sdf')
		self.sdf.set('version', "1.4")
		
		world = Et.SubElement( self.sdf, 'world')
		world.set('name', 'default')
	
	def addSphericalCoords(self, latVal, lonVal, elevationVal = 0.0, headingVal = 0):
		spherical_coordinates = Et.SubElement( self.sdf.find('world'), 'spherical_coordinates')
		
		model = Et.SubElement( spherical_coordinates, 'surface_model')
		model.text = "EARTH_WGS84"
		
		lat = Et.SubElement( spherical_coordinates, 'latitude_deg')
		lat.text = str(latVal)
		
		lon = Et.SubElement(spherical_coordinates, 'longitude_deg')
		lon.text = str(lonVal)
		
		elevation = Et.SubElement( spherical_coordinates, 'elevation')
		elevation.text = str(elevationVal)
		
		heading = Et.SubElement( spherical_coordinates, 'heading_deg')
		heading.text = str(headingVal)
	
	def addModule( self, moduleName):
		includeModule = Et.SubElement( self.sdf.find('world'), 'include')
		includeUri = Et.SubElement( includeModule, 'uri')
		includeUri.text = "model://" + moduleName
			
	def addRoad( self, roadName):
		road = Et.SubElement( self.sdf.find('world'), 'road')
		road.set( 'name', roadName)
	
	def setRoadWidth( self, width, roadName):
		allRoads = self.sdf.find('world').findall('road') 
		roadWanted = [ road for road in allRoads if road.get('name') == roadName]
		roadWidth = Et.SubElement( roadWanted[0] , 'width')
		roadWidth.text = str(width)
	
	def addRoadPoint( self, point, roadName):
		allRoads = self.sdf.find('world').findall('road') 
		roadWanted = [ road for road in allRoads if road.get('name') == roadName]
		roadPoint = Et.SubElement( roadWanted[0], 'point')
		roadPoint.text = str(point[0]) + " " + str(point[1]) + " " + str(point[2])
	
	def writeToFile( self, filename ):
		roughXml = Et.tostring( self.sdf, 'utf-8')
		reparsed = minidom.parseString(roughXml)
	    	prettyXml = reparsed.toprettyxml(indent="\t")	
		
		outfile = open( filename, "w")
		outfile.write( prettyXml )
		outfile.close()
def test():	
  p = GetSDF()
  p.addModule( "sun")	
  p.addModule("ground_plane")
  p.addSpericalCoords(37.85,-122.5)
  p.addRoad( "my_road")
  p.setRoadWidth( 7.34, "my_road")
  p.addRoadPoint( [0 , 0, 0], "my_road")
  p.addRoadPoint( [100, 0, 0], "my_road")	
  p.writeToFile( "outclass.sdf")
	
