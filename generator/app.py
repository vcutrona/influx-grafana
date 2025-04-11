import os
import time
import random
import signal

from datetime import datetime, timezone
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

class Generator:
    token = os.getenv("INFLUXDB_TOKEN")
    bucket = os.getenv("INFLUXDB_BUCKET")
    org = os.getenv("INFLUXDB_ORG")
    host = os.getenv("INFLUXDB_HOST")

    exit_app = False
    signals = {
        signal.SIGINT: 'SIGINT',
        signal.SIGTERM: 'SIGTERM'
    }

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

        if not all([self.token, self.bucket, self.org, self.host]):
            print("Please set the INFLUXDB_TOKEN, INFLUXDB_BUCKET, INFLUXDB_ORG, and INFLUXDB_HOST environment variables.")
            exit(1)
        
        print("Connecting to InfluxDB...")
        print(f"Host: {self.host}")
        print(f"Token: {self.token}")
        print(f"Bucket: {self.bucket}")
        print(f"Org: {self.org}")
        self.client = InfluxDBClient(url=self.host, token=self.token)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
    
    def exit_gracefully(self, signum, frame):
        print(f"\nReceived {self.signals[signum]} signal")
        self.exit_app = True
    
    def stop(self):
        print("Stopping generator...")
        self.client.close()
        exit(0)
    
    def generate(self):
        clock = datetime.now(timezone.utc)

        point1 = Point("chlorine").tag("mode", "auto").field("value", random.gauss(40, 3)).time(clock, WritePrecision.NS)
        point2 = Point("temperature").tag("mode", "auto").field("value", random.gauss(20, 5)).time(clock, WritePrecision.NS)

        print(f"New point: {point1}")
        self.write_api.write(bucket=self.bucket, org=self.org, record=point1)
        print(f"New point: {point2}")
        self.write_api.write(bucket=self.bucket, org=self.org, record=point2)

        if random.random() < .03:
            point = Point("chlorine").tag("mode", "manual").field("value", random.gauss(40, 3)).time(datetime.now(timezone.utc), WritePrecision.NS)
            print(f"New point: {point}")
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)
        
        if random.random() < .05:
            point = Point("temperature").tag("mode", "manual").field("value", random.gauss(20, 5)).time(datetime.now(timezone.utc), WritePrecision.NS)
            print(f"New point: {point}")
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)

        time.sleep(1)


if __name__ == '__main__':
    generator = Generator()
    while not generator.exit_app:
        generator.generate()
    
    generator.stop()
