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
  inputParser.add_option( '-m', '--syncMeta', action='store_true', help='Syncrhonize metadata to a remote host.' )
  inputParser.add_option( '-v', '--visualizeGraph', action='store', default='', help='Visualize the project graph.' )
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
    metaDataManager.createRemoteWorkSpace( 'remote0', '/absolute/path/of/project/home/on/remote0' )
    exit()

  #If the metadata is already initialized, load the project script modules
  sys.path.append( './.scientificProjectManager/scripts' )
  from steps import *
  from utilities import *

  #Load the metadata, objects of metadata classes are named as
  #ProjectInfo       pI;
  #ProjectLog        pL;
  #ProjectGraph      pG;
  #DataFileOperation dO;
  #meta = ( pI, pL, pG, dO )
  meta = metaDataManager.loadMetaData()

  #Synchronize metadata to remote host
  if options.syncMeta:
    metaDataManager.syncMetadataToRemote( 'remote0' )
   
  #Visualize the project graph
  if options.visualizeGraph != '':
    graphVisualizer = SPM.GraphVisualizer( meta[2] )
    if options.visualizeGraph == 'all':
      graphVisualizer.showAll(True)
    elif options.visualizeGraph == 'up':
      graphVisualizer.showUpStreams( args[0], True ) 
    exit()

  ############Scripting area for research steps##########
  #Select motifs
  if options.step == 'indent':
    idXML = Step_indentXML( meta, 'particles', 'particles', 'data/externalData/particles' ) 
    #idXML.clear()
    idXML.createIODataSets()
    idXML.run()

  if options.step == 'wc1':
    wc1 = Step_wordCount( meta, 'particles', 'particles', 'data/externalData/particles' )
    #wc1.clear()
    wc1.createIODataSets()
    wc1.run()

  if options.step == 'wc2':
    wc2 = Step_wordCount( meta, 'particlesIndent', 'particlesIndent', 'data/Step_indentXML/outputDataSets/particles' )
    #wc2.clear()
    wc2.createIODataSets()
    wc2.run()
