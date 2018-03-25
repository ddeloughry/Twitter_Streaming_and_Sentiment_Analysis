FROM python:3-alpine
ADD Analysis.py /
RUN pip install pika
RUN pip install pymongo
RUN pip install textblob
CMD ["python","Analysis.py"]