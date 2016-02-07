#!/usr/bin/env python2
'''
ProjectGraph manages the project graph
'''

import os.path
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
    nodeNorm = os.path.normpath( a_node )
    for node in self.xmlRoot.find('nodes'):
      if node.text == nodeNorm:
        return ( True, node ) 
    return ( False, None )

  def edgeExists( self, a_nodeIn, a_nodeOut ):
    '''
    Return true if an edge exists. Also return the edge element if it exists.
    '''
    nodeInNorm  = os.path.normpath( a_nodeIn )
    nodeOutNorm = os.path.normpath( a_nodeOut )
    for edge in self.xmlRoot.find('edges'):
      if edge.find('from').text == nodeInNorm and edge.find('to').text == nodeOutNorm:
        return ( True, edge )
    return ( False, None )

  def getDegree( self, a_node, a_type ):
    '''
    Return the indegree or outdegree of a node
    '''
    nodeNorm = os.path.normpath( a_node )
    if not self.nodeExists( nodeNorm ):
      raise Exception( 'The node '+nodeNorm+' does not exist!' )

    degree = 0 
    for edge in self.xmlRoot.find('edges'):
      if a_type == 'i' and edge.find('to').text == nodeNorm:
        degree += 1
      if a_type == 'o' and edge.find('from').text == nodeNorm:
        degree += 1
    return degree
   
  def addNode( self, a_node ):
    '''
    Add a node to the graph
    '''
    nodeNorm = os.path.normpath( a_node )
    if self.nodeExists( nodeNorm )[0]:
      return
    node      = ET.SubElement( self.xmlRoot.find('nodes'), 'node' )
    node.text = nodeNorm
    return  
 
  def addEdge( self, a_nodeIn, a_nodeOut ):
    '''
    Add an edge to the graph
    '''
    nodeInNorm  = os.path.normpath( a_nodeIn )
    nodeOutNorm = os.path.normpath( a_nodeOut )
    if self.edgeExists( nodeInNorm, nodeOutNorm )[0]:
      return
    
    self.addNode( nodeInNorm )
    self.addNode( nodeOutNorm )
    edge      = ET.SubElement( self.xmlRoot.find('edges'), 'edge' )
    nIn       = ET.SubElement( edge, 'from' )
    nOut      = ET.SubElement( edge, 'to' )
    nIn.text  = nodeInNorm
    nOut.text = nodeOutNorm
    return

  def removeNode( self, a_node ):
    '''
    Remove a node if it exists.
    '''
    nodeNorm = os.path.normpath( a_node )
    #Remove all edges to this node, while keep all edges from this node. This won't mess up dependency
    for edge in self.xmlRoot.find('edges'):
      if edge.find('to').text == nodeNorm:
        self.removeEdge( edge.find('from').text, nodeNorm ) 
    #Remove the node
    nodeExists = self.nodeExists( nodeNorm )
    if not nodeExists[0]:
        return
    self.xmlRoot.find('nodes').remove( nodeExists[1] )
    return

  def removeEdge( self, a_nodeIn, a_nodeOut ):
    '''
    Remove an edge if it exists.
    '''
    nodeInNorm  = os.path.normpath( a_nodeIn )
    nodeOutNorm = os.path.normpath( a_nodeOut )
    edgeExists = self.edgeExists( nodeInNorm, nodeOutNorm )
    if edgeExists[0]:
      self.xmlRoot.find('edges').remove( edgeExists[1] ) 
    return
