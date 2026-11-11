import csv, time
import boto3

table = boto3.resource("dynamodb").Table("iocs")

count = 0
start = time.time()
with open("iocs.csv", newline="") as f, table.batch_writer() as batch:
    reader = csv.reader(f)
    next(reader)                                  # skip the header line "url"
    for row in reader:
        batch.put_item(Item={"url": row[0]})      # one item per URL
        count += 1
        if count % 25 == 0:
            time.sleep(1)                         # 25 writes per second = our capacity
        if count % 5000 == 0:
            print("Written so far:", count, "| minutes:", round((time.time() - start) / 60, 1))

print("Loaded", count)