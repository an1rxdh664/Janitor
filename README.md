# Codebase "Janitor" & Documentation Bot
An AI-powered GitHub App designed to automate the maintenance of project documentation. The "Janitor" listens to Pull Request events, analyzes code changes (diffs) and generates summaries to keep your documentation in sync with your code.

## Overview
This project solves the "stale documentation" problem by integrating directly into the CI/CD workflow. It identifies the intent behind code changes and updates PR descriptions or documentation files automatically.

## System Architecture
The project is built with a modular "separation of concerns" approach :

* **`app.py`**: The FastAPI entry point handling webhook routing and event gating.
* **`core/github_client.py`**: Manages authenticated REST API calls to fetch raw diffs and post comments.
* **`core/security.py`**: Validates incoming payloads using HMAC SHA-256 signatures.
* **`utils/logger.py`**: Handles structured event logging for monitoring bot activity.

## Tech Stack

* **Backend:** Python 3.10+, FastAPI
* **AI Engine:** Llama 3.1 8B
* **APIs:** GitHub REST API (v3)
* **Security:** HMAC Signature Verification & Environment Secret Management

## Features

* **Secure Webhooks**: Verified communication between GitHub and FastAPI.
* **Private Repo Access**: Authenticated diff extraction using Fine-grained PATs.
* **AI Summarization**: Converts messy Git diffs into clean, human-readable summaries.
* **Automated PR Updates**: Directly modifies PR descriptions with AI-generated insights.

## Setup and Installation
1. **Clone the Repo**:
   ```
   bash
   git clone [https://github.com/your-username/codebase-janitor.git](https://github.com/your-username/codebase-janitor.git)
   cd codebase-janitor
   ```
2. **Environment Variables**:
  Create a `.env` file and add your credentials :

    ```
    GITHUB_AUTH_TOKEN=your_personal_access_token
    WEBHOOK_SECRET=your_webhook_secret
    OPENAI_API_KEY=your_ai_api_key
    ```
4. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```
5. **Run the Server**:
   ```
   uvicorn app:app --reload
   ```
   * Additional note - You also need to set up `ngrok` for this API to generate a working URL to provide into the Webhook URL section of your repository.
      
      * Just setup `ngrok` and run it, in a separate terminal, on the `port` your API service is running on, For Example :
      
         * If my API is running on port `8000` :

              ```
              ngrok http 8000
              ``` 

* Message : This project is still under development, i am still working on making new changes but if anyone would like to contribute then please do so, Thankyou for checking my project.

Anirudh Kushwah, Mail : anirudhhh637@gmail.com
