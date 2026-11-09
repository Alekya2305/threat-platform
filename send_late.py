import json
from confluent_kafka import Producer

producer = Producer({"bootstrap.servers": "localhost:9092"})

BAD_URL = "http://60.18.57.168:55371/i"     # a known-bad URL (e126's), so the join would match

events = [
    {"event_id": "ontime1", "ts": "2026-11-09T10:20:00", "user": "erin", "url": BAD_URL},
    {"event_id": "late1",   "ts": "2026-11-09T09:00:00", "user": "erin", "url": BAD_URL},
]

for event in events:
    producer.produce("logs", key=event["user"], value=json.dumps(event))

producer.flush()
print("Sent", len(events), "events")