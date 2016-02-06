#!/usr/bin/env python2
'''
ProjectGraph manages the project graph
'''

import xml.etree.ElementTree as ET
import utilities

class ProjectGraph():
  '''
  ProjectGraph manages the project graph
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
    return

  def destruct( self ):
    self.saveToFile( self.xmlFileName )
    return

  def nodeExists( self, a_node ):
    '''
    Return true if a node exists. Also return the node element if it exists.
    '''
    for node in self.xmlRoot.find('nodes'):
      if node.text == a_node:
        return ( True, node ) 
    return ( False, None )

  def edgeExists( self, a_nodeIn, a_nodeOut ):
    '''
    Return true if an edge exists. Also return the edge element if it exists.
    '''
    for edge in self.xmlRoot.find('edges'):
      if edge.find('from').text == a_nodeIn and edge.find('to').text == a_nodeOut:
        return ( True, edge )
    return ( False, None )
   
  def addNode( self, a_node ):
    '''
    Add a node to the graph
    '''
    if self.nodeExists( a_node )[0]:
      return
    node      = ET.SubElement( self.xmlRoot.find('nodes'), 'node' )
    node.text = a_node
    return  
 
  def addEdge( self, a_nodeIn, a_nodeOut ):
    '''
    Add an edge to the graph
    '''
    if self.edgeExists( a_nodeIn, a_nodeOut )[0]:
      return
    
    self.addNode( a_nodeIn )
    self.addNode( a_nodeOut )
    edge      = ET.SubElement( self.xmlRoot.find('edges'), 'edge' )
    nIn       = ET.SubElement( edge, 'from' )
    nOut      = ET.SubElement( edge, 'to' )
    nIn.text  = a_nodeIn
    nOut.text = a_nodeOut
    return

  def removeNode( self, a_node ):
    '''
    Remove a node if it exists.
    '''
    nodeExists = self.nodeExists( a_node )
    if not nodeExists[0]:
        return
    self.xmlRoot.find('nodes').remove( nodeExists[1] )
    #Also remove all edges attached to this node
    for node in self.xmlRoot.find('nodes'):
      self.removeEdge( a_node, node.text ) 
      self.removeEdge( node.text, a_node ) 
    return

  def removeEdge( self, a_nodeIn, a_nodeOut ):
    '''
    Remove an edge if it exists.
    '''
    edgeExists = self.edgeExists( a_nodeIn, a_nodeOut )
    if edgeExists[0]:
      self.xmlRoot.find('edges').remove( edgeExists[1] ) 
    return
