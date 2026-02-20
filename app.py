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

def log_events(req_headers, body_json):
    print("Inside event logger\n")

    try:
        number = body_json["number"]

        full_name = body_json["repository"]["full_name"]

        action = body_json["action"]
        
        event_type = req_headers["x-github-event"]
        
        diff_url = body_json["pull_request"]["diff_url"]
        
        head_sha = body_json["pull_request"]["head"]["sha"]

        print(f"Full Repository Name : {full_name} | Number : {number} | Action : {action}\n")
        print(f"Event Type : {event_type}\nDiff URL : {diff_url}\nHead SHA : {head_sha}\n")

    except Exception as e:
        return {"Error": "Some error occured while fetching data"}


    print("\nLogging done\n")

    return

@app.get("/info")
async def get_info():
    about_info = ""
    return about_info

@app.post("/webhook")
async def get_webhook(request: Request):  
    try:
        # STORE HEADERS
        req_headers = request.headers

        # Request body sent by the Github POST is in bytes which needs to be converted into a JSON string
        req_body_bytes = await request.body()

        # But first it needs to be decoded into the utf-8 standard encoding
        body_bytes_decoded = req_body_bytes.decode("utf-8")
        body_json = json.loads(body_bytes_decoded)


        log_events(req_headers, body_json)

    except json.JSONDecodeError as e:
        return {"Error": "Invalid JSON Data", "details": str(e)}
    

    return {"message": "Bytes successfully decoded into JSON string."}