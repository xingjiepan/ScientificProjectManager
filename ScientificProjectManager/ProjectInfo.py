#!/usr/bin/env python2
'''
ProjectInfo manages the project information
'''

import xml.etree.ElementTree as ET
import utilities

class ProjectInfo():
  '''
  ProjectInfo manages the project information
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

  def hostExists( self, a_host ):
    '''
    Return True if a host exists in the host list
    '''
    if None == self.xmlRoot.find('hostInfo').find('hostList').find( a_host ):
      return False
    else:
      return True

  def addHost( self, a_host, a_homeAbsPath ):
    '''
    Add a host to the host list
    '''
    if self.hostExists( a_host ):
      return
    else:
      newHost          = ET.SubElement( self.xmlRoot.find('hostInfo').find('hostList'), a_host )
      homeAbsPath      = ET.SubElement( newHost, 'homeAbsPath' )
      homeAbsPath.text = a_homeAbsPath
    return

  def getCurrentHost( self ):
    '''
    Get the name of current host 
    '''
    return  self.xmlRoot.find('hostInfo').find('currentHost').text

  def setCurrentHost( self, a_host ):
    '''
    Set the current host
    '''
    #If the host is in the list, set it to be the current host
    if self.hostExists( a_host ): 
      self.xmlRoot.find('hostInfo').find('currentHost').text = a_host
    else:
      raise Exception( 'The host '+ a_host +' is not in the host list!' ) 
    return

  def getHomeAbsPath( self, a_host='' ):
    '''
    Return the absolute path of the project home at a_host. 
    '''
    if a_host == '':
      host = self.getCurrentHost()
    elif not self.hostExists( a_host ):
      raise Exception( 'The host '+a_host+' does not exist!' )
    else:
      host = a_host
    return self.xmlRoot.find('hostInfo').find('hostList').find( host.strip() ).find('homeAbsPath').text
