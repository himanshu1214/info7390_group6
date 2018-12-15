FROM ubuntu

# System requirements
RUN apt-get update && apt-get install -y python3-pip

RUN pip3 install --upgrade pip

# Bundle object sources
RUN mkdir /WayfairFinal
ADD flask /WayfairFinal/flask
ADD RegressionModel.ipynb /WayfairFinal
ADD new_prediction.ipynb /WayfairFinal
ADD productsComp_products.ipynb /WayfairFinal
ADD regression_data.csv /WayfairFinal
ADD script.sh /WayfairFinal

# Install python3 modules
RUN pip3 install \
    jupyter \
    pandas \
    h2o \
    flask \
    sklearn 

# start download origination and perforation data
CMD /bin/bash WayfairFinal/script.sh
