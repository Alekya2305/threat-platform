import boto3
from fastapi import FastAPI

app = FastAPI()
ddb = boto3.client("dynamodb")          # created once at startup, reused by every request

@app.get("/check")
def check(value: str):
    resp = ddb.get_item(TableName="iocs", Key={"url": {"S": value}})   # look up one key
    return {"value": value, "known_bad": "Item" in resp}                # Item only comes back if found