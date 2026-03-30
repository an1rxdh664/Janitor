import json
from fastapi import FastAPI, Request

from core.security import verify_request
from core.github_client import fetch_diff_data, createURL, regenerate_description, send_patch
from utils.logger import event_logger
from ai.engine import generate_summary

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
        
        decoded_request_body = req_body_bytes.decode("utf-8") 
        request_body = json.loads(decoded_request_body)
        
        if(request_status):
            event = req_headers.get("x-github-event")
            action = request_body.get("action")

            if(event == "ping"):
                return {"message": "Event was a ping event"}
            
            if(action == "closed"):
                return {"message": "The PR was closed"}
            
            elif(action == "edited"):
                return {"message": "The PR information was edited"}
            
            elif(event == "pull_request" and (action == "opened" or action == "synchronize")):
                url = createURL(request_body)                
                data = fetch_diff_data(url)
                
                generated_summary = generate_summary(data)
                pr_description_body = request_body.get("pull_request").get("body")

                regenerated_pr_body = regenerate_description(pr_description_body, generated_summary)

                patch_response = send_patch(url, regenerated_pr_body)

                if patch_response == 401:
                    return {"message": f"{patch_response}: Bad Token"}
                elif patch_response == 403:
                    return {"message": f"{patch_response}: Permission Issue"}
                elif patch_response == 422:
                    return {"message": f"{patch_response}: Invalid Payload"}

                return {"message": f"{patch_response} : Successfull"}
            else:
                return {"message": "Event was neither a pr nor a ping event"}    
        else:
            return {"Validation Error": "The secret key could not be validated"}

    except Exception as e:
        return {"Error": "Invalid Data", "details": str(e)}