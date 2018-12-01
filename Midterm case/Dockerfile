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

# Install python modules
RUN pip3 install \
  auto-sklearn \
  jupyter \
  robobrowser \
  lxml \
  missingno \
  plotly

# start download origination and perforation data
CMD python3 /midterm-case/Part1-Download.py \
   && jupyter notebook --ip 0.0.0.0 --no-browser --allow-root --notebook-dir='/midterm-case'