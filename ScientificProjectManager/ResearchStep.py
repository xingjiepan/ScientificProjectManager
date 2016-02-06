#!/usr/bin/env python2
'''
ResearchStep is the base class of actual research steps
'''

import os

class ResearchStep(object):
  '''
  ResearchStep is the base class of actual research steps.
  This class is in fact an abstract class because its functions work only when the following variables are defined in its child class.
  pI                      #Object of ProjectInfo
  pL                      #Object of ProjectLog
  pG                      #Object of ProjectGraph
  dO                      #Object of DataFileOperation
  stepDir                 #Directory for this research step
  dependencyList          #List of dependency data set directories
  inputDataSet            #Name of input data set
  outputDataSet           #Name of output data set

  The child classes should also implement the following functions.
  __init__()              #The name of input and output data sets are determined in the initialization step
  createIODataSets()      #Create the input output data set. Note that it's possible for one input dataset to have multiple output data sets.
  run()                   #Either run the job locally or submit it to a cluster. It takes a tasklist as argument to determine which task to run    
   
  '''
  def __init__( self, a_meta, a_stepDir, a_inputDataSet, a_outputDataSet ):
    self.pI            = a_meta[0]
    self.pL            = a_meta[1]
    self.pG            = a_meta[2]
    self.dO            = a_meta[3]
    self.stepDir       = a_stepDir
    self.inputDataSet  = a_inputDataSet
    self.outputDataSet = a_outputDataSet
    return
 
  def relativeToHome( self, a_addr, a_io ):
    '''
    Given an address relative to the input data set or output data set, return its relative address to the project home 
    '''
    if a_io == 'i':
      return os.path.join( self.stepDir, 'inputDataSets', self.inputDataSet, a_addr )  
    elif a_io == 'o':
      return os.path.join( self.stepDir, 'outputDataSets', self.outputDataSet, a_addr )  
    return
 
  def addStepToGraph( self ):
    '''
    Add this step into the project graph
    '''
    self.pG.addEdge( self.relativeToHome('','i'), self.relativeToHome('','o') )
    for d in self.dependencyList:
      self.pG.addEdge( d, self.relativeToHome('','i') )  
    return

  def createIODirs( self, iDirList, oDirList ):
    '''
    Create directories for the input output data sets   
    '''
    #If the step directory does not exists, create it
    if not self.dO.exists( self.stepDir ):
      self.dO.mkdir( self.stepDir ) 
      self.dO.mkdir( os.path.join( self.stepDir, 'inputDataSets' ) ) 
      self.dO.mkdir( os.path.join( self.stepDir, 'outputDataSets' ) ) 
     
    #Create directories for outputDataSet 
    if self.dO.exists( self.relativeToHome('', 'o') ):
      raise Exception( 'The output data set '+self.relativeToHome('', 'o')+' already exists!' ) 
    else:
      self.dO.mkdir( self.relativeToHome('', 'o') )
      for d in oDirList:
        self.dO.mkdir( self.relativeToHome( d, 'o' ) )

    #Add this step to the project graph
    self.addStepToGraph()    

    #Create directories for inputDataSet, do nothing if the input dataset already exists 
    if self.dO.exists( self.relativeToHome('', 'i') ):
      return
    else:
      self.dO.mkdir( self.relativeToHome('', 'i') )
      for d in iDirList:
        self.dO.mkdir( self.relativeToHome( d, 'i' ))

    return 
