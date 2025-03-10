FROM python:3.11.8-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev gcc python3-dev
COPY /requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade pip -r /requirements.txt

COPY /app /app
WORKDIR /app

ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
