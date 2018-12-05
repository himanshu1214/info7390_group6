FROM ubuntu

# System requirements
RUN apt-get update && apt-get install -y \
  build-essential \
  curl \
  python3-pip \
  swig \
  && rm -rf /var/lib/apt/lists/*

# Upgrade pip, install dependencies needed for auto-sklearn
RUN pip3 install --upgrade pip
RUN curl https://raw.githubusercontent.com/automl/auto-sklearn/master/requirements.txt \
  | xargs -n 1 -L 1 pip3 install

# Bundle app source
RUN mkdir /midterm-case
ADD Part1-Data_wrangling.ipynb /midterm-case
ADD Part1-Download.py /midterm-case
ADD Archive /midterm-case
ADD Part12-data_wrangling.ipynb /midterm-case
ADD script.sh /midterm-case

# Install python modules
RUN pip3 install \
  auto-sklearn \
  jupyter \
  robobrowser \
  lxml \
  missingno \
  plotly

# start download origination and perforation data
CMD /bin/bash midterm-case/script.sh