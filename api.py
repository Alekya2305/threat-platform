from fastapi import FastAPI
from iocstore import IOCStore

app = FastAPI()

store = IOCStore()            
store.load("urlhaus.csv")     

@app.get("/check")
def check(value: str):
    return {"value": value, "known_bad": store.is_bad(value)}