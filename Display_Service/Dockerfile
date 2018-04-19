FROM python:3-alpine
ADD Display.py /
RUN pip install pymongo
RUN pip install flask
RUN pip install dateutil
CMD ["python","Display.py"]