FROM python:3.10-alpine

WORKDIR /app

ENV PORT="8000"

ENV DURATION=300

ENV APIKEY="API_KEY"

ENV CITY="tehran"

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
