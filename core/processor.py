import json, httpx

from core.security import verify_request
from core.github_client import createURL, fetch_diff_data, regenerate_description
from ai.engine import generate_summary

from config import GITHUB_FINE_GRAINED_TOKEN

# FUNCTION TO RECIEVE DATA FROM GITHUB
async def receive_data(request):
    req_headers = dict(request.headers)        
    req_body_bytes = await request.body()

    request_status = verify_request(req_headers, req_body_bytes)

    if not request_status:
        return {
            "status": False,
            "error": "Invalid Signature"
        }
    
    decoded_request_body = req_body_bytes.decode("utf-8") 
    request_body = json.loads(decoded_request_body)

    event = req_headers.get("x-github-event")
    action = request_body.get("action")

    return {
        "headers": req_headers,
        "status": request_status,
        "body": request_body,
        "event": event,
        "action": action
    }


# FUNCTION TO SEND IT TO GITHUB
async def send_data(url, body):
    async with httpx.AsyncClient() as client:
        response = await client.patch(
                url = url,
                headers = {
                    "Authorization": f"Bearer {GITHUB_FINE_GRAINED_TOKEN}",
                    "Accept": "application/vnd.github+json",
                    "Content-Type": "application/json"
                },
                json = {
                    "body": body
                },
                timeout=15.0
            )
    
    return response.status_code

# FUNCTION TO GENERATE SUMMARY AND DESCRIPTION
async def construct_data(data):

    status = data.get('status')
    body = data.get('body')
    event = data.get('event')
    action = data.get('action')
    
    if(status):
        if(event == "ping"):
            print("Event was a ping event")
            return
        
        if(action == "closed"):
            print("The PR was closed")
            return
        
        elif(action == "edited"):
            print("The PR information was edited")
            return
        
        elif event == "pull_request" and action in ["opened", "synchronize"]:
            url = createURL(body)                
            data = fetch_diff_data(url)
            
            generated_summary = generate_summary(data)
            pr_description_body = body.get("pull_request").get("body")

            regenerated_pr_body = regenerate_description(pr_description_body, generated_summary)

            patch_response = await send_data(url, regenerated_pr_body)
            
            if patch_response == 401:
                print(f"{patch_response}: Bad Token")
                return
            elif patch_response == 403:
                print(f"{patch_response}: Permission Issue")
                return
            elif patch_response == 422:
                print(f"{patch_response}: Invalid Payload")
                return
            
            print(f"{patch_response} : Successfull")
            return
        
        else:
            print("Event was neither a pr nor a ping event")
            return    
    
    else:
        print("The secret key could not be validated")
        return