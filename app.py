import json
from fastapi import FastAPI, Request
from pydantic import BaseModel

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

def event_logger(req_headers, body_json):
    print("Inside event logger\n")

    try:
        event = req_headers.get("x-github-event")

        if(event == "ping"):
            print("Ping Event, Successfull")
            return {"Connection successful": "Ping event successfully logged."}
        
        elif(event == "pull_request"):
            print("Event is a pull request : \n")
            
            pr_number = body_json.get("number")
            repository_full_name = body_json.get("repository").get("full_name")
            action_type = body_json.get("action")
            diff_url = body_json.get("pull_request").get("diff_url")
            head_sha = body_json.get("pull_request").get("head").get("sha")
            
            print("Details of the PR : \n")
            print(f"Pull request number : {pr_number}")
        
            print(f"Full Repository Name : {repository_full_name} | Action : {action_type}\n")
            print(f"Diff URL : {diff_url}\nHead SHA : {head_sha}\n")

        else:
            return {"message": "Event is neither a ping event or a pull request"}

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

        # But first it needs to be decoded into the utf-8 standard encoding
        body_bytes_decoded = req_body_bytes.decode("utf-8")
        body_json = json.loads(body_bytes_decoded)

        event_logger(req_headers, body_json)

    except json.JSONDecodeError as e:
        return {"Error": "Invalid JSON Data", "details": str(e)}
    

    return {"message": "Bytes successfully decoded into JSON string."}