import json
import boto3
import pyarrow.parquet as pq

QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/744672512316/alerts"

rows = pq.read_table("out/alerts").to_pylist()     # Day 5 Parquet folder → list of dicts
sqs = boto3.client("sqs")

sent = 0
for row in rows:
    sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=json.dumps(row))   # one alert = one message
    sent += 1

print("Sent", sent, "alerts")