FROM python:3.6.5

# Update
RUN pip install --upgrade pip

# Install app dependencies
RUN pip install boto3
RUN pip install BeautifulSoup4
RUN pip install pandas
RUN pip install lxml
RUN pip install requests

# Bundle app source
ADD missing_data.py /

CMD ["python", "./missing_data.py"]