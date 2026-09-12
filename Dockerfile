FROM python:3.9-slim-buster

LABEL org.opencontainers.image.title="InfraMonitor"
LABEL org.opencontainers.image.description="Python Flask Linux Infrastructure Monitoring System"
LABEL org.opencontainers.image.source="https://github.com/Rizwana200/InfraMonitor"

ARG srcDir=src

WORKDIR /app

COPY $srcDir/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY $srcDir/run.py .
COPY $srcDir/app ./app

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]

