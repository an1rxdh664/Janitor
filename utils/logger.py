
# JUST A BASIC EVENT LOGGER FOR THE PROGRAM

def event_logger(body_json, diff_data):
    print("Inside event logger\n")
    try:
            pr_number = body_json.get("number")
            repository_full_name = body_json.get("repository").get("full_name")
            action_type = body_json.get("action")
            diff_url = body_json.get("pull_request").get("diff_url")
            head_sha = body_json.get("pull_request").get("head").get("sha")
            
            print(f"Repository : {body_json.get("repository")}\n")

            print("Details of the PR : \n")
            print(f"Pull request number : {pr_number}")
        
            print(f"Full Repository Name : {repository_full_name} | Action : {action_type}\n")
            print(f"Diff URL : {diff_url}\nHead SHA : {head_sha}\nDiff Data : {diff_data}")
            # CHECKING IF THE DIFF DATA IS GETTING RECIEVED OR NOT NOT COMPLETED YET

    except Exception as e:
        return {"Error": "Some error occured while fetching data"}
    print("\nLogging done\n")

    return