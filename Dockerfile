FROM python:3.10.2

RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade pip

WORKDIR /app

ADD . /app

ENTRYPOINT ["python"]
CMD ["main.py"]
