import json
import os
import requests

def as_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def as_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()    

def send_email_notification(content):
    sandbox = os.getenv('MAILGUN_SANDBOX')
    api_address = f"https://api.mailgun.net/v3/{sandbox}/messages"
    to = f"Leo Fagundes <{os.getenv("EMAIL_ADDRESS")}>"

    try:
        requests.post(api_address,  		
            auth=("api", os.getenv('MAILGUN_API_KEY')),
            data={"from": f"Mailgun Sandbox <postmaster@{sandbox}>",
                "to": to,
                "subject": "LeoGPT",
                "text": content}
        )
    except Exception as e:
        print(f"Error when sending email: {e}")