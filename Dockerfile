FROM python:3.7-alpine

WORKDIR /code
COPY . .

RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV FLASK_APP app.main:flask_app
ENV FLASK_RUN_HOST 0.0.0.0

CMD ["flask", "run"]