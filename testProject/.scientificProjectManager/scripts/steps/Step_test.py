from ScientificProjectManager import ResearchStep
import os

class Step_test( ResearchStep ):
  def __init__( self, a_meta, a_inputDataSet, a_outputDataSet, a_manDataSet ):
    super(Step_test, self).__init__( a_meta, 'data/Step_test', a_inputDataSet, a_outputDataSet ) 
    self.manDataSet     = a_manDataSet
    self.dependencyList = [ a_manDataSet ]
    return

  def createIODataSets( self ):
    self.createIODirs( ['someIputs'], ['someOutputs'] )
    self.dO.lns( os.path.join( self.manDataSet, 'test' ), self.relativeToHome( 'freshData', 'i') ) 
    return 
