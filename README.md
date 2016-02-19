# ScientificProjectManager

## What does ScientificProjectManager do?
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
│   ├── externalData/                     # Datasets from outset 
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
└── SMPInterface.py  
```
(In the above directory tree, names end with *, e.g. projectHome*, are user defined names.) 
