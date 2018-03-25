FROM python:3-alpine
ADD Streamer.py /
RUN pip install pika
RUN pip install tweepy
RUN pip install argparse
CMD ["python","Streamer.py"]