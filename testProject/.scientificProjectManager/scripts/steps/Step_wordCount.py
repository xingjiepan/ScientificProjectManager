from ScientificProjectManager import ResearchStep
import os
import subprocess

class Step_wordCount( ResearchStep ):
  '''
  Count word 
  '''
  def __init__( self, a_meta, a_inputDataSet, a_outputDataSet, a_sourceSet):
    super(Step_wordCount, self).__init__( a_meta, 'data/Step_wordCount', a_inputDataSet, a_outputDataSet )
    self.sourceSet        = a_sourceSet
    self.dependencyList   = [ a_sourceSet ]
    return

  def createIODataSets( self ):
    self.createIODirs( [], [] )
    sourceFileList = self.dO.ls( self.sourceSet )
    for f in sourceFileList:
      self.dO.lns( os.path.join( self.sourceSet, f ), self.relativeToHome( '', 'i' ) )
    return

  def run( self ):
    inputFileList = self.dO.ls( self.relativeToHome( '', 'i' ) )
    for f in inputFileList:
      with open( self.absAddr( 'wc_'+f+'.txt', 'o' ), 'w' ) as fOut:
        subprocess.call( [ 'wc', self.absAddr( f, 'i' ) ], stdout=fOut )    
    return
 
