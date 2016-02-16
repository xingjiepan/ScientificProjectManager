#!/usr/bin/env python2
'''
This file provides some utilities for the rest of ScientificProjectManager classes   
'''

import xml.etree.ElementTree as ET
import xml.dom.minidom as xmlDom
import os
import subprocess
from sets import Set

def getPrettyXmlString( a_element ):
  '''
  Get a XML string with indent
  '''
  #Get the string and strip all white spaces
  roughString = ET.tostring( a_element, 'utf-8' )
  stripedString = ''
  for line in roughString.split('\n'):
    if not line.strip() == '':
      stripedString += line.strip()
  #Get the pretty xml string
  reparsed    = xmlDom.parseString( stripedString )
  return reparsed.toprettyxml( indent='  ' )

def getRsyncIncludeList( a_fileList ):
  '''
  Get a nonredundent list of include flags for a list of files
  '''
  iSet = Set()
  for f in a_fileList:
    fSplit = f.split('/')
    for j in range( len(fSplit)-1 ):
      iSet.add( '/'.join( fSplit[0:j+1] )+'/' )
    iSet.add(  f+'**' )
 
  includeList = []
  for i in iSet:
    includeList.append( '--include' )
    includeList.append( i )
  return includeList

def syncFilesToRemote( a_currentHomeAbs, a_fileList, a_remoteHost, a_remoteHomeAbs ):
  '''
  Synchronize a set of files to the remote host.
  File addresses specified a_fileList should be relative addresses to the a_currentHomeAbs. 
  '''
  subprocess.call( ['rsync', '--copy-links']+getRsyncIncludeList( a_fileList )+[ '--exclude', '*', '-avrz', a_currentHomeAbs+'/', a_remoteHost+':'+a_remoteHomeAbs+'/'] ) 
  return

def syncFilesFromRemote( a_currentHomeAbs, a_fileList, a_remoteHost, a_remoteHomeAbs ):
  '''
  Synchronize a set of files from the remote host.
  File addresses specified a_fileList should be relative addresses to the a_currentHomeAbs. 
  '''
  subprocess.call( ['rsync', '--copy-links']+getRsyncIncludeList( a_fileList )+[ '--exclude', '*', '-avrz', a_remoteHost+':'+a_remoteHomeAbs+'/', a_currentHomeAbs+'/'] ) 
  return
