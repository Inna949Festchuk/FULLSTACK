FROM python:3.11.8-slim-bookworm
RUN apt-get update && apt-get install -y libpq-dev gcc python3-dev --no-install-recommends
COPY /requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY /app /app
WORKDIR /app

ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]
