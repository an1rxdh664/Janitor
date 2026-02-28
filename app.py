import json
from fastapi import FastAPI, Request
from pydantic import BaseModel

import os
from dotenv import load_dotenv

import hmac, hashlib, base64
from hmac import compare_digest

load_dotenv() # LOAD VARIABLES FROM .env
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

description = "This API endpoint is currently made for testing purposes of my janitor model."

app = FastAPI(
    title="Webhook Endpoint tester",
    description=description,
    version="0.0.1",
    contact={
        "name": "Anirudh Kushwah",
        "email": "anirudhhh637@gmail.com"
    }
)

def verify_request(headers, body, secret: str):
    # RETRIEVING THE GITHUB SIGNATURE HEADER
    signature_header = headers.get('x-hub-signature-256')

    # ENCODE THE SECRET INTO BYTES
    secret_bytes = secret.encode('utf-8')

    computated_signature = "sha256=" + hmac.new(
        key=secret_bytes,
        msg=body,
        digestmod=hashlib.sha256
    ).hexdigest()

    return compare_digest(computated_signature, signature_header)

def event_logger(body_json):
    print("Inside event logger\n")
    try:            
            pr_number = body_json.get("number")
            repository_full_name = body_json.get("repository").get("full_name")
            action_type = body_json.get("action")
            diff_url = body_json.get("pull_request").get("diff_url")
            head_sha = body_json.get("pull_request").get("head").get("sha")
            
            print("Details of the PR : \n")
            print(f"Pull request number : {pr_number}")
        
            print(f"Full Repository Name : {repository_full_name} | Action : {action_type}\n")
            print(f"Diff URL : {diff_url}\nHead SHA : {head_sha}\n")

    except Exception as e:
        return {"Error": "Some error occured while fetching data"}
    print("\nLogging done\n")
    
    return

@app.get("/")
async def server_info():
    return {
        "Description": description,
        "Creator": "Anirudh Kushwah",
        "Contact Details": {
            "E-mail" : "anirudhhh637@gmail.com",
            "Linked-In" : "https://www.linkedin.com/in/anirudh-kushwah-b885483a3/",
            "Twitter / X" : "https://x.com/anirxdh14"
        }
    }

@app.post("/webhook")
async def get_webhook(request: Request):  
    try:
        # STORE HEADERS
        req_headers = request.headers
        
        # Request body sent by the Github POST is in bytes which needs to be converted into a JSON string
        req_body_bytes = await request.body()

        # VERIFY IF THE REQEUST IS VALID OR NOT
        request_status = verify_request(req_headers, req_body_bytes, WEBHOOK_SECRET)
        
        if(request_status):
            # EVENT OCCURED
            event = req_headers.get("x-github-event")

            # HANDLE THE PING EVENT
            if(event == "ping"):
                return {"message": "Event was a ping event"}
            
            # EVENT GATING
            elif(event == "pull_request"):
                # But first the body needs to be decoded into the utf-8 standard encoding
                body_bytes_decoded = req_body_bytes.decode("utf-8")
                body_json = json.loads(body_bytes_decoded)

                event_logger(body_json)

                return {"message": "Event was a PR"}
            else:
                return {"message": "Event was neither a pr nor a ping event"}    
        else:
            return {"Validation Error": "The secret key could not be validated"}


    except Exception as e:
        return {"Error": "Invalid Data", "details": str(e)}