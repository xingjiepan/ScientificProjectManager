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
    print self.graph.nodes()
    return

  def show( self ):
    nx.draw_networkx( self.graph )
    plt.show()
    return
