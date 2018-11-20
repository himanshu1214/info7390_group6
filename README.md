# info7390_group6
Advance data science and architecture
## Case1 Working with EDGAR datasets
  Working with Edgar datasets: Wrangling, Pre-processing and exploratory data analysis.  
  
  **EDGAR**, the Electronic Data Gathering, Analysis, and Retrieval system.performs automated collection, validation, indexing,     acceptance, and forwarding of submissions by companies and others who are required by law to file forms with the U.S. Securities and Exchange Commission (the "SEC")
   ### Problem 1: Data wrangling Edgar data from text files
   * **config.ini** 
       *--store CIK, acc_no data*
   * **Dockerfile** 
       *--docker config for docker*
       ```
       docker build -t parse_file .
       docker run -ti parse_file
       ```
       -i stands for interactive mode and -t will allocate a pseudo terminal for us.<br/>
       In this way, you can input aws key and secret in docker via keyboard
   * **parse_file.py**
       *--parse file python cource code*
   ### Problem 2: Missing Data Analysis
   * **Dockerfile** *--docker config for docker*
       ```
       docker build -t missing_data .
       docker run -ti missing_data
       ```
       -i stands for interactive mode and -t will allocate a pseudo terminal for us.<br/>
       In this way, you can input aws key and secret in docker via keyboard
   * **missing_data.py** *--missing dat python source code*

## EDA and Data Visualization Practice work
  Conduct an exploratory data analysis using Python packages (seaborn, matplotlib) to understand the dataset.
  
## Case2 Machine learning with Energy datasets
  AdaptiveAlgo Systems Inc. works on solutions to build algorithms and platforms to address energy modeling challenges.  
  
  With the knowledge of energy consumed by various equipment, seasonality and attributes like temperature and humidity, a machine learning model could be used to predict aggregate energy use.

