import json
import boto3

QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/744672512316/alerts"
sqs = boto3.client("sqs")

handled = 0
while True:
    resp = sqs.receive_message(QueueUrl=QUEUE_URL, MaxNumberOfMessages=10, WaitTimeSeconds=10)
    msgs = resp.get("Messages", [])                     # list of messages ([] if none)
    if not msgs:
        break                                           # empty → stop (a real worker keeps looping forever)
    for m in msgs:
        alert = json.loads(m["Body"])                   # text → dict
        print("ALERT:", alert["user"], alert["url"])    # "handle" it (real: Slack / ticket)
        sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=m["ReceiptHandle"])   # done → remove it
        handled += 1

print("Handled", handled, "alerts")