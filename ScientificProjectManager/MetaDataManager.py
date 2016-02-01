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
from DirForest         import DirForest  
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
    subprocess.call( [ 'mkdir', '.scientificProjectManager' ] )
    subprocess.call( [ 'mkdir', '.scientificProjectManager/scratch' ] )
    subprocess.call( [ 'mkdir', '.scientificProjectManager/scripts' ] )
    subprocess.call( [ 'mkdir', '.scientificProjectManager/scripts/steps' ] )
    subprocess.call( [ 'mkdir', '.scientificProjectManager/scripts/showData' ] )
    subprocess.call( [ 'mkdir', '.scientificProjectManager/scripts/utilities' ] )
    
    #Create metadata files 
    self.createNewProjectInfo( a_currentHost )
    self.createNewDirForest( a_currentHost )
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
    host             = ET.SubElement( hostList, 'host'        )
    currentHost.text = a_currentHost
    host.text        = a_currentHost

    #Save the projectInfo.xml file
    fXml = open('.scientificProjectManager/projectInfo.xml', 'w')
    fXml.write( utilities.getPrettyXmlString( projectInfo ) )
    fXml.close() 
    return

  def createNewDirForest( self, a_currentHost ):
    '''
    create a new dirForest.xml file
    '''
    #If the projectInfo.xml file is already been created, return
    if os.path.exists( '.scientificProjectManager/dirForest.xml' ):
      print "The .scientificProjectManager/dirForest.xml is already been created!"
      return

    #Create the XML tree of the directory forest
    dirForest        = ET.Element('dirForest')
    dirTree          = ET.SubElement( dirForest, 'dirTree'  )
    host             = ET.SubElement( dirTree, 'host'       )
    homeAbsPath      = ET.SubElement( dirTree, 'homeAbsPath')
    home             = ET.SubElement( dirTree, 'home'       )
    subdirs          = ET.SubElement( home   , 'subdirs'    )
    files            = ET.SubElement( home   , 'files'      )
    dataDir          = ET.SubElement( subdirs, 'data'       ) 
    dataSubdirs      = ET.SubElement( dataDir, 'subdirs'    )
    dataFiles        = ET.SubElement( dataDir, 'files'      )
    eDataDir         = ET.SubElement( dataSubdirs, 'externalData' ) 
    eDataSubdirs     = ET.SubElement( eDataDir, 'subdirs'   )
    eDataFiles       = ET.SubElement( eDataDir, 'files'     )
    host.text        = a_currentHost
    homeAbsPath.text = os.path.abspath('.')

    #Save the projectLog.xml file
    fXml = open('.scientificProjectManager/dirForest.xml', 'w')
    fXml.write( utilities.getPrettyXmlString( dirForest ) )
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
    Load metadata from the drictory .scientificProjectManager and return initialized objects of ProjectInfo, DirForest, ProjectLog, ProjectGraph and DataFileOperation 
    '''
    #Create objects of the metadat handlers
    pI = ProjectInfo( '.scientificProjectManager/projectInfo.xml' )
    pL = ProjectLog( '.scientificProjectManager/projectLog.xml' )
    dF = DirForest( '.scientificProjectManager/dirForest.xml', pI, pL)
    pG = ProjectGraph( '.scientificProjectManager/projectGraph.xml' )
    dO = DataFileOperation( pI, pL, dF )
    
    #Register destruct functions 
    atexit.register( pI.destruct )
    atexit.register( pL.destruct )
    atexit.register( dF.destruct )
    atexit.register( pG.destruct )

    #Initialize the metadata
    dF.initializeFromRealDir()
   
    return  ( pI, pL, dF, pG, dO )

  def createRemoteWorkSpace( self, a_host, a_homeAddr ):
    '''
    Create a remote work space on a given host and copy all metadata there.
    '''
    return
