import json
from fastapi import FastAPI, Request
from pydantic import BaseModel

description = ""

app = FastAPI(
    title="Webhook Endpoint tester",
    description=description,
    version="0.0.1",
    contact={
        "name": "Anirudh Kushwah",
        "email": "anirudhhh637@gmail.com"
    }
)

@app.get("/info")
async def get_info():
    about_info = ""
    return about_info

@app.post("/webhook")
async def get_webhook(request: Request):
    
    # Request body sent by the Github POST is in bytes which needs to be converted into a JSON string
    req_body_bytes = await request.body()

    # But first it needs to be decoded into the utf-8 standard encoding
    body_bytes_decoded = req_body_bytes.decode("utf-8")

    try:
        body_json = json.loads(body_bytes_decoded)
    except json.JSONDecodeError as e:
        return {"Error": "Invalid JSON Data", "details": str(e)}
    

    return {"message": "Bytes successfully decoded into JSON string."}

