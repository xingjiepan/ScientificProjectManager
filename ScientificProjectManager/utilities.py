#!/usr/bin/env python2
'''
This file provides some utilities for the rest of ScientificProjectManager classes   
'''

import xml.etree.ElementTree as ET
import xml.dom.minidom as xmlDom


def getPrettyXmlString( a_element ):
  '''
  Get a XML string with indent
  '''
  #Get the string and strip all white spaces
  roughString = ET.tostring( a_element, 'utf-8' )
  stripedString = ''
  for line in roughString.split('\n'):
    if not line.strip() == '':
      stripedString += line.strip()
  #Get the pretty xml string
  reparsed    = xmlDom.parseString( stripedString )
  return reparsed.toprettyxml( indent='  ' )
