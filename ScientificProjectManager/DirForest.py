#!/usr/bin/env python2
'''
DirForest manages the directory forest
'''

import os
import copy
import xml.etree.ElementTree as ET
import utilities

class DirForest():
  '''
  DirForest manages the directory forest
  '''
  def __init__( self, a_xmlFileName, a_projectInfo, a_projectLog ):
    self.xmlFileName = a_xmlFileName
    self.xmlTree     = ET.parse( self.xmlFileName )
    self.xmlRoot     = self.xmlTree.getroot()
    self.pI          = a_projectInfo
    self.pL          = a_projectLog
    self.setCurrentTree()
    return

  def initializeFromRealDir( self ):
    '''
    Initialize the directory tree of the current host such that it matches the real diretroy
    '''
    self.iterativelyInitializeDir( 'data', self.currentTree.find('home').find('subdirs').find('data') )
    return

  def iterativelyInitializeDir( self, a_dirAddr, a_dirElement ):
    '''
    Initialize a directory iteratively. The input directory address should be the relative address to the project home.
    '''
    absDir       = self.currentTree.find('homeAbsPath').text+'/'+a_dirAddr
    filesAndDirs = os.listdir( absDir )
    files        = list( f for f in filesAndDirs if os.path.isfile( absDir+'/'+f ) )
    dirs         = list( d for d in filesAndDirs if os.path.isdir( absDir+'/'+d ) )
   
    #Iterate over all files and add new files to the XML tree. Always update symlink files 
    for f in files:
      if a_dirElement.find('files').find(f) == None or os.path.islink( absDir+'/'+f):
        addr = a_dirAddr+'/'+f
        if a_dirElement.find('files').find(f) == None:
          self.pL.write( self.currentTree.find('host').text, 'Detect manually added file '+addr )
        #Check if the file is a symlink.
        if os.path.islink( absDir+'/'+f ):
          linkAddr = os.path.relpath( os.path.realpath( absDir+'/'+f ), self.currentTree.find('homeAbsPath').text )
        else:
          linkAddr = ''
        self.addFile( addr, a_symLinkAddr=linkAddr )
    
    #Iterate over all subdirectories and add new directories to the XML tree
    for d in dirs: 
     if a_dirElement.find('subdirs').find(d) == None:
       self.pL.write( self.currentTree.find('host').text, 'Detect manually added directory '+a_dirAddr+'/'+d )
       self.addDir( a_dirAddr+'/'+d )
     self.iterativelyInitializeDir( a_dirAddr+'/'+d, a_dirElement.find('subdirs').find(d) ) 
    
    #Iterate over all file subelements and remove obselate elements in the XML tree
    for fileElement in a_dirElement.find('files'):
      if not fileElement.tag in files:
        self.pL.write( self.currentTree.find('host').text, 'Detect manually removed file '+a_dirAddr+'/'+fileElement.tag )
        a_dirElement.find('files').remove( fileElement )

    #Iterate over all subdirectory elements and remove obselate elements in the XML gree 
    for subdirElement in a_dirElement.find('subdirs'):
      if not subdirElement.tag in dirs:
        self.pL.write( self.currentTree.find('host').text, 'Detect manually removed directory '+a_dirAddr+'/'+subdirElement.tag )
        a_dirElement.find('subdirs').remove( subdirElement )
    return

  def saveToFile( self, a_fileName ):
    xmlFile = open( a_fileName, 'w' )
    xmlFile.write( utilities.getPrettyXmlString( self.xmlRoot ) )
    xmlFile.close()
  
  def destruct( self ):
    self.saveToFile( self.xmlFileName )
    return

  def treeExists( self, a_host ):
    '''
    Return true if a directory tree exists 
    '''
    treeExists = False
    for dirTree in self.xmlRoot:
      if a_host == dirTree.find('host').text:
        treeExists = True 
    return treeExists

  def getTree( self, a_host ):
    '''
    Get the tree for the a_host
    '''
    if not self.treeExists( a_host ):
      raise Exception( 'The directory tree for the host '+ a_host +' does not exist!' )
    else:
      for dirTree in self.xmlRoot:
        if a_host == dirTree.find('host').text:
          return dirTree
    return 
  
  def setCurrentTree( self ):
    '''
    Set the current tree the tree of the current host 
    '''
    currentHost = self.pI.getCurrentHost()
    self.currentTree = self.getTree( currentHost ) 
    return

  def addressExists( self, a_addr, a_host='' ):
    '''
    Return true if an address exists in the XML tree. Also return the type of the address
    '''
    #Find the tree to search
    if a_host == '':
      host = self.pI.getCurrentHost()
    else:
      host = a_host
    dirTree = self.getTree( host )
    
    splitAddr = a_addr.split('/')
    elementName = splitAddr[ len(splitAddr) -1 ]
    #Go to the directory that contains the required element
    currentDir = dirTree.find('home')
    for i in range( len(splitAddr) - 1 ):
      currentDir = currentDir.find('subdirs').find( splitAddr[i] )
      if currentDir == None:
        return (False, '')
    #Get the required element
    for d in currentDir.find('subdirs'):
      if d.tag == elementName:
        return ( True, 'dir' )
    for f in currentDir.find('files'):
      if f.tag == elementName:
        return ( True, 'file' )
    return (False, '')
 
  def addressToElement( self, a_addr, a_host='' ):
    '''
    Given the address of a directory or file, return its element.
    The addres should be the relative address to the project home. 
    '''
    #Find the tree to search
    if a_host == '':
      host = self.pI.getCurrentHost()
    else:
      host = a_host
    dirTree = self.getTree( host )
    
    splitAddr = a_addr.split('/')
    elementName = splitAddr[ len(splitAddr) -1 ]
    #Go to the directory that contains the required element
    currentDir = dirTree.find('home')
    for i in range( len(splitAddr) - 1 ):
      currentDir = currentDir.find('subdirs').find( splitAddr[i] )
      if currentDir == None:
        raise Exception( 'The directory '+'/'.join( splitAddr[0:i+1] )+' does not exist!' )
    #Get the required element
    for d in currentDir.find('subdirs'):
      if d.tag == elementName:
        return d
    for f in currentDir.find('files'):
      if f.tag == elementName:
        return f

    raise Exception( 'No such file or directory ' + a_addr )
    return

  def getAbsAddr( self, a_addr, a_host='' ):
    '''
    Given the address of a directory or file, return its absolute address
    '''
    #Find the tree to search
    if a_host == '':
      host = self.pI.getCurrentHost()
    else:
      host = a_host
    return self.getTree( host ).find('homeAbsPath').text +'/'+a_addr

  def splitNameAndParent( self, a_addr ):
    '''
    Given the address of a directory or file, return its name and itsparent address.
    '''
    #Parse the address
    splitAddr = a_addr.split('/')
    name      = splitAddr[ len(splitAddr) - 1 ]
    #Get the parent directory
    parentDirAddr = '/'.join( splitAddr[0:len(splitAddr)-1] )
    return (name, parentDirAddr) 

  def addFile( self, a_fileLongName, a_host='', a_symLinkAddr='' ):
    '''
    Add a file to the specified directory tree.
    The file address should be the relative address to the project home.
    '''
    #Check if the file is a symlink file
    if a_symLinkAddr == '':
      isLink = False
    else:
      isLink = True
    #Get the file name and parent directory
    (fileName, parentDirAddr) = self.splitNameAndParent( a_fileLongName )
    parentDir     = self.addressToElement( parentDirAddr, a_host ) 
    #Add the file. Update the symlink information if the file is already there
    for f in parentDir.find('files'):
      if f.tag == fileName:
        f.find('isLink').text   = str(isLink)
        f.find('linkAddr').text = a_symLinkAddr
        return
    fN      = ET.SubElement( parentDir.find('files'), fileName )
    iL      = ET.SubElement( fN, 'isLink' )
    lA      = ET.SubElement( fN, 'linkAddr' )
    iL.text = str(isLink)
    lA.text = a_symLinkAddr
    return

  def addDir( self, a_dirLongName, a_host='' ):
    '''
    Add a directory to the specified directory tree.
    The directory address should be the relative address to the project home.
    '''
    #Get the file name and parent directory
    (dirName, parentDirAddr) = self.splitNameAndParent( a_dirLongName )
    parentDir     = self.addressToElement( parentDirAddr, a_host ) 
    #Add the directory. Do nothing if the directory is already there
    for d in parentDir.find('subdirs'):
      if d.tag == dirName:
        return
    dN = ET.SubElement( parentDir.find('subdirs'), dirName )
    sD = ET.SubElement( dN, 'subdirs' ) 
    fS = ET.SubElement( dN, 'files' ) 
    return

  def remove( self, a_addr, a_host='' ):
    '''
    Remove a file or directory from the directory tree.
    The address should be the relative address to the project home. 
    '''
    #Do nothing if the address doesn't exist at all
    addrExist = self.addressExists( a_addr, a_host )
    if not addrExist[0]:
      return
    #Get the file name and parent directory
    (addrName, parentDirAddr) = self.splitNameAndParent( a_addr )
    parent     = self.addressToElement( parentDirAddr, a_host ) 
    #Remove the element 
    if addrExist[1] == 'file':
      parent.find('files').remove( parent.find('files').find(addrName) ) 
    elif addrExist[1] == 'dir':
      parent.find('subdirs').remove( parent.find('subdirs').find(addrName) ) 
    return

  def copy( self, a_origin, a_target, a_host='' ):
    '''
    Copy a file or directory from a_origin to a_target.
    The address should be the relative address to the project home. 
    '''
    #Check if the origin and target exist
    originExists = self.addressExists( a_origin, a_host )
    targetExists = self.addressExists( a_target, a_host )
    if not originExists[0]:
      raise Exception( 'The file or directory '+a_origin+' does not exist!' )
    #Prevent copy a directory to itself
    if a_origin == a_target and originExists[1] == 'dir':
      raise Exception( 'Cannot copy the directory '+ a_origin +' to itself!' )
    #Get the names of origin and target and theri parents
    (originName, originParentName) = self.splitNameAndParent( a_origin )
    (targetName, targetParentName) = self.splitNameAndParent( a_target )
    #If target exists and is a directory, set a_target to be the parent
    if targetExists[0] and targetExists[1] == 'dir':
      targetName       = originName
      targetParentName = a_target
    realTargetExists = self.addressExists( targetParentName+'/'+targetName ) 
    #Prevent directory to be rewrited
    if realTargetExists[0] and realTargetExists[1] == 'dir':
      raise Exception( 'Cannot overwrite the directory '+targetParentName+'/'+targetName )
    if realTargetExists[0] and realTargetExists[1] == 'file' and originExists[1] == 'dir':
      raise Exception( 'Cannot overwrite the file '+targetParentName+'/'+targetName+' with the directory '+a_origin )
    #Copy the origin element
    originElementCopy = copy.deepcopy( self.addressToElement( a_origin ) )
    #Rename the copied origin
    originElementCopy.tag = targetName
    targetParent = self.addressToElement( targetParentName, a_host )
    #Remove the target element
    self.remove( targetParentName+'/'+targetName, a_host )
    #Add the origin to target parent
    if originExists[1] == 'dir':
      targetParent.find('subdirs').append( originElementCopy ) 
    if originExists[1] == 'file':
      targetParent.find('files').append( originElementCopy ) 
    return

  def move( self, a_origin, a_target, a_host='' ):
    '''
    Move a file or directory from a_origin to a_target.
    The address should be the relative address to the project home.
    '''
    self.copy( a_origin, a_target, a_host )
    self.remove( a_origin, a_host )
    return

