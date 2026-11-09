import csv
import json
from confluent_kafka import Producer

producer = Producer({"bootstrap.servers": "localhost:9092"})

# Load the bad URLs into a set (fast "in" checks, like IOCStore on Day 2)
bad = set()
with open("iocs.csv", newline="") as f:
    reader = csv.reader(f)
    next(reader)                                # skip the header line "url"
    for row in reader:
        bad.add(row[0])

sent = 0          # counter for me: all messages sent
bad_sent = 0      # counter for me: bad events sent (for reconciliation)
first_bad = None

with open("fake_logs.csv", newline="") as f:
    reader = csv.reader(f)
    next(reader)                                # skip the header line
    for i, row in enumerate(reader, start=1):   # i = 1, 2, 3, ...
        event = {
            "event_id": "e" + str(i),
            "ts": row[0],
            "user": row[1],
            "url": row[2],
        }
        producer.produce("logs", key=event["user"], value=json.dumps(event))   # → Kafka
        producer.poll(0)
        sent += 1
        if event["url"] in bad:
            bad_sent += 1
            if first_bad is None:
                first_bad = event               # remember the first bad event

# Planted duplicate: the first bad event again (same event_id + same ts)
producer.produce("logs", key=first_bad["user"], value=json.dumps(first_bad))
sent += 1

producer.flush()                                # wait until everything has reached Kafka
print("Sent", sent, "events,", bad_sent, "bad, + 1 duplicate of", first_bad["event_id"])