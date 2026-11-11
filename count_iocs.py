import time
import boto3

ddb = boto3.client("dynamodb")
paginator = ddb.get_paginator("scan")                    # Scan = read every item

total = 0
for page in paginator.paginate(TableName="iocs", Select="COUNT",
                               PaginationConfig={"PageSize": 1000}):
    total += page["Count"]                               # items counted in this page
    time.sleep(2.5)                                      # stay under 5 reads/second

print("Items in DynamoDB:", total)