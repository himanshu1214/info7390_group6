# info7390_group6

## Assignment1
  Working with Edgar datasets: Wrangling, Pre-processing and exploratory data analysis
   ### Problem 1: Data wrangling Edgar data from text files
   * **config.ini** 
       *--store CIK, acc_no data*
   * **Dockerfile** 
       *--docker config for docker*
       ```
       docker build -t parse_file .
       docker run -ti parse_file
       ```
   * **parse_file.py**
       *--parse file python cource code*
   ### Problem 2: Missing Data Analysis
   * **Dockerfile** *--docker config for docker*
       ```
       docker build -t missing_data .
       docker run -ti missing_data
       ```
   * **missing_data.py** *--missing dat python source code*

## EDA and Data Visualization Practice work

  Conduct an exploratory data analysis using Python packages (seaborn, matplotlib) to understand the dataset.
