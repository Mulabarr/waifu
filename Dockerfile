FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /waifu

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /waifu/