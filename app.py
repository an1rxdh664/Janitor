import json
from fastapi import FastAPI, Request

# IMPORTING FUNCTIONS FROM OTHER MODULES
from core.security import verify_request
from core.github_client import fetch_diff_data
from utils.logger import event_logger


description = "This API endpoint is currently made only for testing purposes of my janitor model."

app = FastAPI(
    title="Webhook Endpoint tester",
    description=description,
    version="0.0.1",
    contact={
        "name": "Anirudh Kushwah",
        "email": "anirudhhh637@gmail.com"
    }
)

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
        request_status = verify_request(req_headers, req_body_bytes)
        
        if(request_status):
            # EVENT OCCURED
            event = req_headers.get("x-github-event")

            # HANDLE THE PING EVENT
            if(event == "ping"):
                return {"message": "Event was a ping event"}
            
            # EVENT GATING
            elif(event == "pull_request"):
                # But first the body needs to be decoded into the utf-8 standard encoding
                decodedBodyBytes = req_body_bytes.decode("utf-8")
                jsonBody = json.loads(decodedBodyBytes)

                diff_data = await fetch_diff_data(jsonBody.get("pull_request").get("diff_url"))
                
                # OPTIONAL FUNCTION TO LOG EVENTS
                event_logger(jsonBody, diff_data)

                return {"message": "Event was a PR"}
            else:
                return {"message": "Event was neither a pr nor a ping event"}    
        else:
            return {"Validation Error": "The secret key could not be validated"}


    except Exception as e:
        return {"Error": "Invalid Data", "details": str(e)}