# a small operating system
FROM python:3.11.5-slim
RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED True
ENV HOST 0.0.0.0
ENV PORT 3000
ENV TZ=Etc/GMT-7

RUN apt-get update && apt-get install -y \
    curl \
    build-essential 

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD exec gunicorn --bind :$PORT --workers 2 --threads 8 --timeout 0 app:app
