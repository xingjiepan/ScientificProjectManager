#!/usr/bin/env python2
'''
MetaDataManager manages the metadata of a scientific project
'''

import os
import subprocess
import xml.etree.ElementTree as ET
import utilities
import time
import atexit
from ProjectInfo       import ProjectInfo  
from ProjectLog        import ProjectLog  
from ProjectGraph      import ProjectGraph  
from DataFileOperation import DataFileOperation 

class MetaDataManager():
  '''
  MetaDataManager manages the metadata of a scientific project
  '''
  def __init__( self ):
    return
  
  def init( self, a_currentHost ):
    '''
    Create meta data for a research project
    '''
    #If the metadata directory is already been created, return
    if os.path.exists( '.scientificProjectManager' ):
      print "The directory .scientificProjectManager is already been created!"
      return 
    
    #Create data and metadata directories 
    subprocess.call( [ 'mkdir', 'data' ] )
    subprocess.call( [ 'mkdir', 'data/externalData' ] )
    subprocess.call( [ 'mkdir', 'data/manuallyProcessedData' ] )
    subprocess.call( [ 'mkdir', '.scientificProjectManager' ] )
    subprocess.call( [ 'mkdir', '.scientificProjectManager/scratch' ] )
    subprocess.call( [ 'mkdir', '.scientificProjectManager/scripts' ] )
    subprocess.call( [ 'mkdir', '.scientificProjectManager/scripts/steps' ] )
    subprocess.call( [ 'mkdir', '.scientificProjectManager/scripts/showData' ] )
    subprocess.call( [ 'mkdir', '.scientificProjectManager/scripts/utilities' ] )
    
    #Create metadata files 
    self.createNewProjectInfo( a_currentHost )
    self.createNewProjectLog( a_currentHost )
    self.createNewProjectGraph()
    return

  def createNewProjectInfo( self, a_currentHost ):
    '''
    create a new projectInfo.xml file
    '''
    #If the projectInfo.xml file is already been created, return
    if os.path.exists( '.scientificProjectManager/projectInfo.xml' ):
      print "The .scientificProjectManager/projectInfo.xml is already been created!"
      return

    #Create the XML tree of the project information
    projectInfo      = ET.Element('projectInfo')
    hostInfo         = ET.SubElement( projectInfo, 'hostInfo' )
    currentHost      = ET.SubElement( hostInfo, 'currentHost' )
    hostList         = ET.SubElement( hostInfo, 'hostList'    )
    host             = ET.SubElement( hostList, a_currentHost )
    homeAbsPath      = ET.SubElement( host, 'homeAbsPath'     )
   
    currentHost.text = a_currentHost
    homeAbsPath.text = os.path.abspath('.')

    #Save the projectInfo.xml file
    fXml = open('.scientificProjectManager/projectInfo.xml', 'w')
    fXml.write( utilities.getPrettyXmlString( projectInfo ) )
    fXml.close() 
    return
  
  def createNewProjectLog( self, a_currentHost ):
    '''
    create a new projectLog.xml file
    '''
    #If the projectLog.xml file is already been created, return
    if os.path.exists( '.scientificProjectManager/projectLog.xml' ):
      print "The .scientificProjectManager/projectLog.xml is already been created!"
      return

    #Create the XML tree of the project log
    projectLog = ET.Element('projectLog')
    record     = ET.SubElement( projectLog, 'record' )
    timeE      = ET.SubElement( record, 'time'       )
    host       = ET.SubElement( record, 'host'       )
    event      = ET.SubElement( record, 'event'      )
    timeE.text = time.strftime('%Y_%m_%d_%H_%M_%S')
    host.text  = a_currentHost
    event.text = "Create metadata"

    #Save the projectLog.xml file
    fXml = open('.scientificProjectManager/projectLog.xml', 'w')
    fXml.write( utilities.getPrettyXmlString( projectLog ) )
    fXml.close() 
    return

  def createNewProjectGraph( self ):
    '''
    create a new projectGraph.xml file
    '''
    #If the projectGraph.xml file is already been created, return
    if os.path.exists( '.scientificProjectManager/projectGraph.xml' ):
      print "The .scientificProjectManager/projectGraph.xml is already been created!"
      return

    #Create the XML tree of the project graph
    projectGraph = ET.Element('projectGraph')
    nodes        = ET.SubElement( projectGraph, 'nodes' )
    edges        = ET.SubElement( projectGraph, 'edges' )

    #Save the projectGraph.xml file
    fXml = open('.scientificProjectManager/projectGraph.xml', 'w')
    fXml.write( utilities.getPrettyXmlString( projectGraph ) )
    fXml.close() 
    return

  def loadMetaData( self ):
    '''
    Load metadata from the drictory .scientificProjectManager and return initialized objects of ProjectInfo, ProjectLog, ProjectGraph and DataFileOperation 
    '''
    #Create objects of the metadat handlers
    self.pI = ProjectInfo( '.scientificProjectManager/projectInfo.xml' )
    self.pL = ProjectLog( '.scientificProjectManager/projectLog.xml' )
    self.pG = ProjectGraph( '.scientificProjectManager/projectGraph.xml' )
    self.dO = DataFileOperation( self.pI, self.pL )
    
    #Register destruct functions 
    atexit.register( self.pI.destruct )
    atexit.register( self.pL.destruct )
    atexit.register( self.pG.destruct )

   
    return  ( self.pI, self.pL, self.pG, self.dO )

  def syncMetadataToRemote( self, a_host ):
    '''
    Synchronize metadata to the remote host.
    Metadata must be load before calling this function 
    '''
    self.pI.destruct()
    self.pL.destruct()
    self.pG.destruct()
    utilities.syncFilesToRemote( self.pI.getHomeAbsPath(), ['SMPInterface.py','.scientificProjectManager'], a_host, self.pI.getHomeAbsPath(a_host) )
    return

  def createRemoteWorkSpace( self, a_host, a_homeAddr ):
    '''
    Create a remote work space on a given host and copy all metadata there.
    '''
    if self.pI.hostExists( a_host ):
      print 'The remote host '+a_host+' already exists!'
      return
    self.pI.addHost( a_host, a_homeAddr )
    currentHost    = self.pI.getCurrentHost()
    currentHomeAbs = self.pI.getHomeAbsPath() 

    #This is a trick to create a empty data directory in the remote host
    subprocess.call( [ 'rsync', '-av', os.path.join( currentHomeAbs, '.scientificProjectManager/scratch' ), a_host+':'+os.path.join(a_homeAddr,'data') ] )  
    
    #Temporarily change the current host into the remote host
    self.pI.setCurrentHost( a_host )
    self.pI.saveToFile( self.pI.xmlFileName )
    #Synchronize the metadata and the interface to the remote host
    utilities.syncFilesToRemote( currentHomeAbs, ['SMPInterface.py','.scientificProjectManager'], a_host, a_homeAddr)

    #Change the currenthost name back
    self.pI.setCurrentHost( currentHost )
     
    return
