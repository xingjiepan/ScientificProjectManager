#!/usr/bin/env python2
'''
DataFileOperation provides a set of methods to manipulate files while keep the modifications being tracked   
'''

import os
import xml.etree.ElementTree as ET
import utilities
import subprocess
import re

class DataFileOperation():
  '''
  DataFileOperation provides a set of methods to manipulate files   
  '''
  def __init__( self, a_projectInfo, a_projectLog ):
    self.pI = a_projectInfo
    self.pL = a_projectLog
    return

  def getAbsAddr( self, a_addr, a_host='' ):
    '''
    Turn a relative address to absolute address
    '''
    return os.path.join( self.pI.getHomeAbsPath( a_host ), a_addr )

  def exists( self, a_addr ):
    '''
    Return true if a file or directory exists  
    The file address should be the relative address to the project home.
    '''
    return os.path.exists( self.getAbsAddr( a_addr ) )

  def ls( self, a_addr ):
    '''
    List the content of a directory.
    The address should be the relative address to the project home.
    '''
    return os.listdir( self.getAbsAddr( a_addr ) )

  def open( self, a_fileAddr, a_method='r' ):
    '''
    To open a file. 
    The file address should be the relative address to the project home.
    '''
    f = open( self.getAbsAddr( a_fileAddr ), a_method )
    return f

  def rm( self, a_target ):
    '''
    To remove a file or directory.
    The file address should be the relative address to the project home.
    '''
    subprocess.call( [ 'rm', '-r', self.getAbsAddr( a_target ) ] )
    return

  def mkdir( self, a_target ):
    '''
    To make a new directory.
    The file address should be the relative address to the project home.
    '''
    subprocess.call( [ 'mkdir', self.getAbsAddr( a_target ) ] )
    return

  def lns( self, a_origin, a_target ):
    '''
    To symbolic link a file or directory 
    The file address should be the relative address to the project home.
    '''
    subprocess.call( [ 'ln', '-s', self.getAbsAddr( a_origin ), self.getAbsAddr( a_target ) ] )
    return

  def cp( self, a_origin, a_target ):
    '''
    To copy a file or directory. 
    The file address should be the relative address to the project home.
    '''
    subprocess.call( [ 'cp', '-r', self.getAbsAddr( a_origin ), self.getAbsAddr( a_target ) ] )
    return

  def mv( self, a_origin, a_target ):
    '''
    To move a file or directory 
    The file address should be the relative address to the project home.
    '''
    subprocess.call( [ 'mv', self.getAbsAddr( a_origin ), self.getAbsAddr( a_target ) ] )
    return

  def chmod( self, a_mode, a_file ):
    '''
    To changed the mode of a file
    The file address should be the relative address to the project home.
    '''
    subprocess.call( ['chmod', a_mode, self.getAbsAddr( a_file ) ] )
    return

  def syncToRemote( self, a_fileList, a_remoteHost ):
    '''
    Synchronize a list of files to the remote host.
    Addresses of files should be relative to the project home. 
    '''
    currentHomeAbs = self.pI.getHomeAbsPath()
    remoteHomeAbs  = self.pI.getHomeAbsPath( a_remoteHost )
    utilities.syncFilesToRemote( currentHomeAbs, a_fileList, a_remoteHost, remoteHomeAbs ) 
    return

  def syncFromRemote( self, a_fileList, a_remoteHost ):
    '''
    Synchronize a list of files from the remote host.
    Addresses of files should be relative to the project home. 
    '''
    currentHomeAbs = self.pI.getHomeAbsPath()
    remoteHomeAbs  = self.pI.getHomeAbsPath( a_remoteHost )
    utilities.syncFilesFromRemote( currentHomeAbs, a_fileList, a_remoteHost, remoteHomeAbs ) 
    return

  def templateSubstituter( self, a_match ):
    if not a_match.group(1) in self.subDict.keys():
      raise Exception( 'Cannot replace ' + a_match.group(1) +' . No rule is given!' )
    return self.subDict[ a_match.group(1) ]

  def createFileFromTemplate( self, a_template, a_outputFile, a_subDict, a_identifier = '!@#\$' ):
    '''
    Create a file from a template.
    a_template   is the template file address relative to the project home;
    a_outputFile is the output file address relative to the project home;
    a_subDict    is the dictionary that specifies substitutions to the template file. NOTE: the key must only contain word charactors (\w)!;
    a_identifier is the mark that specifies variable places in the template file;  
    '''
    subPattern   = re.compile( a_identifier + '(\w+)' + a_identifier )
    self.subDict = a_subDict    
 
    fTemp = open( self.getAbsAddr(a_template) )
    fOut  = open( self.getAbsAddr(a_outputFile), 'w' )
    for line in fTemp.readlines():
      fOut.write( subPattern.sub( self.templateSubstituter, line ) )
    fTemp.close()
    fOut.close() 
    return

  def saveXMLFile( self, a_xmlElement, a_fOut ):
    '''
    Save an XML element to a file.
    Address of a_fOut should be relative to the project home.
    '''
    with open( self.getAbsAddr(a_fOut), 'w' ) as fOut:
      fOut.write( utilities.getPrettyXmlString( a_xmlElement ) )  
    return
