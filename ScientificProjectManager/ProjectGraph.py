#!/usr/bin/env python2
'''
ProjectGraph manages the project graph
'''

import xml.etree.ElementTree as ET
import utilities

class ProjectGraph():
  '''
  ProjectGraph manages the project graph
  '''
  def __init__( self, a_xmlFileName ):
    self.xmlFileName = a_xmlFileName
    self.xmlTree     = ET.parse( self.xmlFileName )
    self.xmlRoot     = self.xmlTree.getroot()
    return

  def saveToFile( self, a_fileName ):
    xmlFile = open( a_fileName, 'w' )
    xmlFile.write( utilities.getPrettyXmlString( self.xmlRoot ) )
    xmlFile.close()

  def destruct( self ):
    self.saveToFile( self.xmlFileName )
    return
