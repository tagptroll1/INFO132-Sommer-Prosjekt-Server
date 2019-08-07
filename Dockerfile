FROM python:3.7-alpine

WORKDIR /code
COPY . .

RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn
EXPOSE 8000
