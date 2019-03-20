FROM python:3.7
RUN apt-get update && apt-get install -f -y postgresql-client && apt-get clean
ENV PYTHONUNBUFFERED 1
WORKDIR /code
ADD requirements.txt /code
ADD run.sh /code
RUN pip install -r requirements.txt
ADD code/ /code/
