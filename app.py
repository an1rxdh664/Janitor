from fastapi import FastAPI, Request, BackgroundTasks

from core.processor import receive_data, construct_data

description = "This AI Janitor model uses GitHub webhooks to listen for diffs between pull request events and generates a summary of it and sends it back to the PR description"

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
async def get_webhook(request: Request, background: BackgroundTasks):  
    try:
        received_data = await receive_data(request)
        
        if not received_data.get("status"):
            return {
                "status": False,
                "error": "Invalid Signature"
            }

        background.add_task(construct_data, {
            "body": received_data["body"],
            "event": received_data["event"],
            "action": received_data["action"],
            "status": received_data["status"]
        })
        
        return {"message": "Request Recieved, Background processing started"}
    
    except Exception as e:
        return {"Error": "Invalid Data", "details": str(e)}