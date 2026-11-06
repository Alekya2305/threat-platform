import sqlite3
from fastapi import FastAPI

app = FastAPI()

# Open the database once, when the API starts
conn = sqlite3.connect("iocs.db", check_same_thread=False)

@app.get("/check")
def check(value: str):
    # ? = placeholder; the real value goes separately in (value,)
    row = conn.execute("SELECT url FROM iocs WHERE url = ?", (value,)).fetchone()
    # fetchone() gives a row if found, None if not
    return {"value": value, "known_bad": row is not None}