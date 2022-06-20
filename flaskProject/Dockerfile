FROM python:3.10
ADD . /app
WORKDIR /app
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
