FROM python:3.12.10-alpine3.21

RUN pip install influxdb-client==1.48.0

COPY app.py .

CMD ["python", "app.py"]
