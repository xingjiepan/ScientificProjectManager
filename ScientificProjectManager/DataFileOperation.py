#!/usr/bin/env python2
'''
DataFileOperation provides a set of methods to manipulate files while keep the modifications being tracked   
'''

import os
import xml.etree.ElementTree as ET
import utilities
import subprocess

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
