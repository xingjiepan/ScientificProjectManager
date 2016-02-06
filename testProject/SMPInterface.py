#!/usr/bin/env python2
'''
Scripting interface of the ScientificProjectManager
'''

import ScientificProjectManager as SPM
from optparse import OptionParser
import sys

if __name__ == '__main__':
  #Parse the input data
  inputParser = OptionParser()
  inputParser.add_option( '-i', '--init', action='store_true', help='Initialize the metadata.' )
  inputParser.add_option( '-c', '--create', action='store_true', help='Create a remote workspace.' )
  inputParser.add_option( '-s', '--step', action='store', help='Reserch step to run' )
  inputParser.add_option( '-b', '--substep', action='store', help='Research substep to run' )
  (options, args) = inputParser.parse_args()

  #Create the MetaDataManager
  metaDataManager = SPM.MetaDataManager()

  if options.init:
    #Initialize metadata in the directory .scientificProjectManager and create the data directory
    metaDataManager.init( 'myLaptop' )
    exit()

  if options.create:
    metaDataManager.loadMetaData()
    metaDataManager.createRemoteWorkSpace( 'QB3Cluster2', '/netapp/home/xingjiepan/test/SPM' )
    exit()

  #If the metadata is already initialized, load the project script modules
  sys.path.append( './.scientificProjectManager/scripts' )
  from steps import *

  #Load the metadata, objects of metadata classes are named as
  #ProjectInfo       pI;
  #ProjectLog        pL;
  #ProjectGraph      pG;
  #DataFileOperation dO;
  #meta = ( pI, pL, pG, dO )
  meta = metaDataManager.loadMetaData()
   

  ############Scripting area for research steps##########
  if options.step == 'test':
    sTest = Step_test( meta, 'testIn', 'testOut', 'data/data/manuallyProcessedData/man')  
    if options.substep == 'create':
      sTest.createIODataSets()
      








  #f = dO.open( 'data/test.txt', 'w' ) 
  #f.close()
  
  #dO.rm( 'data/test.txt' )
  #dO.mkdir( 'data/new' )
  #dO.lns( 'data/test.txt', 'data/new' )
  #dO.cp( 'data/test.txt', 'data/new/a' )
  #dO.mv( 'data/test.txt', 'data/new/b' )
  #dO.syncToRemote( ['data/externalData'], 'QB3Cluster2' )
  #dO.syncFromRemote( ['data/eular'], 'QB3Cluster2' )
  #print dO.exists( 'data/test.txt1' )

  #pG.addNode( 'node1' )
  #pG.addEdge( 'node1', 'node2' )
  #pG.removeEdge( 'node1', 'node2' )
  #pG.removeNode( 'node1' )

  #pL.write( 'myLaptop', 'textEvent' )
