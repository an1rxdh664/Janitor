import json
from fastapi import FastAPI, Request

from core.security import verify_request
from core.github_client import fetch_diff_data, createURL
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
        req_headers = request.headers        
        req_body_bytes = await request.body()

        request_status = verify_request(req_headers, req_body_bytes)
        
        if(request_status):
            event = req_headers.get("x-github-event")

            if(event == "ping"):
                return {"message": "Event was a ping event"}
            
            elif(event == "pull_request"):
                decoded_request_body = req_body_bytes.decode("utf-8") 
                requestBody = json.loads(decoded_request_body)

                url = createURL(requestBody)                
                data = fetch_diff_data(url)

                return {"message": "Event was a PR"}
            else:
                return {"message": "Event was neither a pr nor a ping event"}    
        else:
            return {"Validation Error": "The secret key could not be validated"}

    except Exception as e:
        return {"Error": "Invalid Data", "details": str(e)}