FROM python:3.10.2

ENV PYTHONPATH=/app
ENTRYPOINT ["pytest"]
CMD []

RUN apt-get update && apt-get upgrade -y

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY requirements.tests.txt /app/requirements.tests.txt
RUN pip install -r requirements.tests.txt

COPY . .
