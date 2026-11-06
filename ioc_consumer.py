import sqlite3
from confluent_kafka import Consumer

# Open (or create) the database file and the table
conn = sqlite3.connect("iocs.db")
conn.execute("CREATE TABLE IF NOT EXISTS iocs (url TEXT PRIMARY KEY)")

# Connect to Kafka as a NEW group, starting from the first message
consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "ioc-saver-2",
    "auto.offset.reset": "earliest",
})
consumer.subscribe(["iocs"])

count = 0
try:
    while True:
        msg = consumer.poll(1.0)          # ask Kafka for a message (wait up to 1s)
        if msg is None:
            continue                       # nothing yet, ask again
        if msg.error():
            print(msg.error())
            continue
        url = msg.value().decode()         # bytes -> text
        conn.execute("INSERT OR IGNORE INTO iocs (url) VALUES (?)", (url,))
        count += 1
        if count % 500 == 0:               # save every 500 messages
            conn.commit()
            print("Read so far:", count)
except KeyboardInterrupt:
    pass                                   # Ctrl+C: stop the loop
finally:
    conn.commit()                          # always save what's left
    conn.close()
    consumer.close()
    print("Read", count, "messages")