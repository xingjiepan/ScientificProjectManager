#!/usr/bin/env python2
'''
DataFileOperation provides a set of methods to manipulate files while keep the modifications being tracked   
'''

import xml.etree.ElementTree as ET
import utilities
import subprocess

class DataFileOperation():
  '''
  DataFileOperation provides a set of methods to manipulate files while keep the modifications being tracked   
  '''
  def __init__( self, a_projectInfo, a_projectLog, a_dirForest ):
    self.pI = a_projectInfo
    self.pL = a_projectLog
    self.dF = a_dirForest
    return

  def open( self, a_fileAddr, a_method='r' ):
    '''
    To open a file while keep it being tracked by the directory forest object
    The file address should be the relative address to the project home.
    '''
    addrExists = self.dF.addressExists( a_fileAddr )
    if not addrExists[0]:
      if a_method == 'w':
        self.dF.addFile( a_fileAddr )
      else:
        raise Exception( 'The file '+a_fileAddr+' does not exist!' )
    elif addrExists[1] == 'dir':
      raise Exception( 'Cannot open the directory '+a_fileAddr+' as a file!' )
 
    f = open( a_fileAddr, a_method )
    return f

  def rm( self, a_target ):
    '''
    To remove a file or directory while keep it being tracked by the directory forest object
    The file address should be the relative address to the project home.
    '''
    subprocess.call( [ 'rm', '-r', self.dF.getAbsAddr( a_target ) ] )
    self.dF.remove( a_target ) 
    return

  def mkdir( self, a_target ):
    '''
    To make a new directory while keep it being tracked by the directory forest object
    The file address should be the relative address to the project home.
    '''
    #Do nothing if there is already a file or directory
    if self.dF.addressExists( a_target )[0]:
      return
    subprocess.call( [ 'mkdir', self.dF.getAbsAddr( a_target ) ] )
    self.dF.addDir( a_target ) 
    return

  def lns( self, a_origin, a_target ):
    '''
    To symbolic link a file or directory while keep it being tracked by the directory forest object
    The file address should be the relative address to the project home.
    '''
    originExists = self.dF.addressExists( a_origin )
    if not originExists[0]:
      raise Exception( 'The file or directory '+a_origin+' does not exist!' )
    elif originExists[1] == 'dir':
      raise Exception( 'Currently do not support symbolic link for directories.' )
    if self.dF.addressExists( a_target )[0]:
      raise Exception( 'Cannot make symbolic link, file or directory '+a_target+' already exists!' )
    
    self.dF.addFile( a_target, a_symLinkAddr=a_origin )
    subprocess.call( [ 'ln', '-s', self.dF.getAbsAddr( a_origin ), self.dF.getAbsAddr( a_target ) ] )
    return

  def cp( self, a_origin, a_target ):
    '''
    To copy a file or directory while keep it being tracked by the directory forest object
    The file address should be the relative address to the project home.
    '''
    if not self.dF.addressExists( a_origin )[0]:
      raise Exception( 'The file or directory '+a_origin+' does not exist!' )
  
    self.dF.copy( a_origin, a_target )#Because the copy in the xml tree is more strigint, this line should come first. 
    subprocess.call( [ 'cp', '-r', self.dF.getAbsAddr( a_origin ), self.dF.getAbsAddr( a_target ) ] )
    return

  def mv( self, a_origin, a_target ):
    '''
    To move a file or directory while keep it being tracked by the directory forest object
    The file address should be the relative address to the project home.
    '''
    if not self.dF.addressExists( a_origin )[0]:
      raise Exception( 'The file or directory '+a_origin+' does not exist!' )
   
    self.dF.move( a_origin, a_target ) #Because the move in the xml tree is more strigint, this line should come first.
    subprocess.call( [ 'mv', self.dF.getAbsAddr( a_origin ), self.dF.getAbsAddr( a_target ) ] )
    return
