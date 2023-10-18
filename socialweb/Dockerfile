FROM python:3.10

WORKDIR /socialwebv2

RUN pip install -U pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
