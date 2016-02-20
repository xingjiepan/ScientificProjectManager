# ScientificProjectManager

## 1. What does ScientificProjectManager do?
The essence of many computational scientific projects is a dynamically growing graph of data processing. Each node is a dataset and each edge is a research step. The basic goal of ScientificProjectManager is to help scientists save their data as nodes of a graph and write their scripts as edges.

ScientificProjectManager provides a set of tools that help users organize their working directory into the following standard form:

```
projectHome*/                             # The home of the project
│
├── .scientificProjectManager/            # A Directory that saves all metadata
│   ├── projectGraph.xml                  # The graph of the project
│   ├── projectInfo.xml                   # General information of the project
│   ├── projectLog.xml                    # The log of the project
│   ├── scratch/
│   └── scripts/
│       ├── showData/                     # Scripts for displaying data
│       ├── steps/                        # Scripts for research steps
│       └── utilities/                    # Scripts provide some basic functions
│
├── data/                                 # A Directory that saves all data
│   ├── externalData/                     # Datasets from outside 
│   │   ├── externalDataset1*/
│   │   ├── externalDataset2*/
│   │   └── .../
│   ├── manuallyProcessedData/            # Manually processed datasets
│   │   ├── manualDataset1*/
│   │   ├── manualDataset2*/
│   │   └── .../
│   ├── step_01*/                         # A user defined step
│   │   ├── inputDataSets/
│   │   │   ├── inputDataset01_01*/
│   │   │   ├── inputDataset01_02*/
│   │   │   └── .../
│   │   └── outputDataSets/
│   │       ├── outputDataset01_01*/
│   │       ├── outputDataset01_02*/
│   │       └── .../
│   ├── step_02*/                         # Another user defined step
│   │   └── .../
│   └── .../
│
└── SMPInterface.py                       # An interface through which users run their research steps 
```
(In the above directory tree, names end with \*, e.g. projectHome\*, are user defined names.)

## 2. A simple tutorial
The following tutorial will tell you how to run ScientificProjectManager. The "research" we want to do here is to make indentation for some XML files and count the number of characters, words and lines inside the XML files.

### 2.1. Install ScientificProjectManager
Clone this repository and add its path to the environment variable PYTHONPATH.

### 2.2. Initialize your project
Copy `testProject/SMPInterface.py` file into a new folder which you want to be your project home. The run
```
./SMPInterface.py -i
```
Then you will find that metadata files along with some data directories are created.

### 2.3. Run some research steps
Copy the folder `testProject/data/externalData/particles` into `data/externalData/` of your new project home. This is your input dataset. Then copy the folder `testProject/.scientificProjectManager/scripts/steps` into `.scientificProjectManager/scripts/` of your new project home. This is the research steps you want to run.

In your new project home, run
```
./SMPInterface.py -i indent
```
Then you will find that a directory `Step_indentXML` is created under `data/` and inside `data/Step_indentXML/outputDataSets/particles/` are the XML files with indentation.

Run
```
./SMPInterface.py -i wc1
```
To count the words of original XML files.

Run
```
./SMPInterface.py -i wc2
```
To count the words of indented XML files.

### 2.4. Visualize the graph of your research project
If the python module `networkx` and `pydot` is install on your computer, you can visualize your project graph by running
```
./SMPInterface.py -v all
```

### 2.5. Think your project as a graph
You may want to ask "Our data is still saved in a directory tree. How do you dare to say they are saved in a graph?" They are saved in a graph because of the following mapping
```
Nodes <- Datasets in data/externalData/
         Datasets in data/manuallyProcessedData/
         Datasets in data/user_defined_step*/outputDataSets/

Edges <- Directory data/user_defined_step*/
         Datasets in data/user_defined_step*/inputDataSets/  
```   
(Names end with \*, e.g. user\_defined\_step\*, are user defined names.)

Think your project as a graph, because it is.

## 3. Important classes of ScientificProjectManager
### 3.1 ProjectInfo
Manages general information of this project, including IP addresses of computers involved and absolute pathes of the project home on different computers. Dumps data to projectInfo.xml.

### 3.2 ProjectGraph
Automatically add/remove nodes and edges of the graph when users add/remove datasets. Dumps data to projectGraph.xml.

### 3.3 ProjectLog
Automatically generate logs for users operation (not finished yet). Dumps data to projectLog.xml.

### 3.4 DataFileOperation
Provide a set of file operations (cp, mv, ls, ln…) with addresses relative to the project home, such that the effect of them are same on different computers.

### 3.5 ResearchStep
Base class of different research steps. Provide functions to manage datasets.

### 3.6 MetaDataManger
Manages all metadata, including projectInfo.xml, projectGraph.xml, projectLog.xml and all research step scripts. 
 
