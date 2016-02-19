from ScientificProjectManager import ResearchStep
import xml.etree.ElementTree as ET
import os

class Step_indentXML( ResearchStep ):
  '''
  Make indentation for XML files
  '''
  def __init__( self, a_meta, a_inputDataSet, a_outputDataSet, a_sourceSet ):
    super(Step_indentXML, self).__init__( a_meta, 'data/Step_indentXML', a_inputDataSet, a_outputDataSet )
    self.sourceSet        = a_sourceSet
    self.dependencyList   = [ a_sourceSet ]
    return

  def createIODataSets( self ):
    self.createIODirs( [], [] )
    # Symlink all xml files in the source dataset into the input dataset 
    sourceFileList = self.dO.ls( self.sourceSet )
    for f in sourceFileList:
      if f.endswith( '.xml' ):
        self.dO.lns( os.path.join( self.sourceSet, f ), self.relativeToHome( '', 'i') )
    return

  def run( self ):
    inputFiles = self.dO.ls( self.relativeToHome( '', 'i' ) )
    for f in inputFiles: 
      xmlTree = ET.parse( self.absAddr( f , 'i' ) )
      xmlRoot = xmlTree.getroot()
      self.dO.saveXMLFile( xmlRoot, self.relativeToHome( f, 'o' ) )
    return
 
