FROM python:3.6.5

# Update
RUN pip install --upgrade pip

# Install app dependencies
RUN pip install boto3
RUN pip install BeautifulSoup4
RUN pip install pandas
RUN pip install lxml

# Bundle app source
ADD parse_file.py /
ADD config.ini /

CMD ["python", "./parse_file.py"]