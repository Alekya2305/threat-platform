import json
import boto3

sqs = boto3.client("sqs")

# 1. the dead letter queue first (the main queue needs to point at it)
dlq_url = sqs.create_queue(QueueName="alerts-dlq")["QueueUrl"]
dlq_arn = sqs.get_queue_attributes(
    QueueUrl=dlq_url, AttributeNames=["QueueArn"]
)["Attributes"]["QueueArn"]

# 2. the main queue, linked to the DLQ
redrive = {"deadLetterTargetArn": dlq_arn, "maxReceiveCount": "3"}
main_url = sqs.create_queue(
    QueueName="alerts",
    Attributes={"RedrivePolicy": json.dumps(redrive), "VisibilityTimeout": "30"},
)["QueueUrl"]

print("alerts:    ", main_url)
print("alerts-dlq:", dlq_url)