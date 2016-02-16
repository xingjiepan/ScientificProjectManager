#!/usr/bin/env python2
'''
GraphVisualizer visualize the project graph
'''
import networkx as nx
import matplotlib.pyplot as plt

class GraphVisualizer():
  '''
  GraphVisualizer visualize the project graph
  '''
  def __init__( self, a_projectGraph ):
    self.graph = nx.DiGraph()
    
    for edge in a_projectGraph.xmlRoot.find('edges'):
      self.graph.add_edge( edge.find('from').text, edge.find('to').text )
    return

  def showAll( self ):
    pos = nx.nx_agraph.graphviz_layout( self.graph, prog='dot' )
    nx.draw_networkx( self.graph, pos )
    plt.show()
    return

  def showUpStreams( self, a_node ):
    '''
    Show the upstream graph of a node.
    '''
    upGraph = nx.DiGraph()
    self.recursiveBuildUpStream( upGraph, a_node )
    pos = nx.nx_agraph.graphviz_layout( upGraph, prog='dot' )
    nx.draw_networkx( upGraph, pos )
    plt.show() 
    return

  def recursiveBuildUpStream( self, a_upGraph, a_node ):
    '''
    Build the upstream graph of a node recursively
    '''
    for upNode in self.graph.predecessors( a_node ):
      if upNode in a_upGraph.nodes():
        a_upGraph.add_edge( upNode, a_node )
        return
      a_upGraph.add_edge( upNode, a_node )
      self.recursiveBuildUpStream( a_upGraph, upNode )
    return
  
