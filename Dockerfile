FROM python:3.9.13-bullseye

ENV GOOGLE_APPLICATION_CREDENTIALS creds.json

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "app.py"]