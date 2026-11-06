import csv
from confluent_kafka import Producer

producer = Producer({"bootstrap.servers": "localhost:9092"})

sent = 0
with open("urlhaus.csv", newline="", encoding="utf-8") as f:
    for row in csv.reader(f):
        if not row or row[0].startswith("#"):
            continue
        url = row[2]
        try:
            producer.produce("iocs", key=url, value=url)
        except BufferError:
            producer.poll(1)                 # waiting area full: wait, then retry
            producer.produce("iocs", key=url, value=url)
        producer.poll(0)                     # let Kafka process deliveries
        sent += 1

producer.flush()                             # wait until everything reached Kafka
print("Sent", sent, "URLs")