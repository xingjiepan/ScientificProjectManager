#!/usr/bin/env python2
'''
ProjectLog manages the project log
'''

import time
import xml.etree.ElementTree as ET
import utilities

class ProjectLog():
  '''
  ProjectLog manages the project log
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

  def write( self, a_host, a_event ):
    '''
    Write an event to the log file
    '''
    timeNow = time.strftime('%Y_%m_%d_%H_%M_%S')
    print timeNow, a_host, a_event
    return 
