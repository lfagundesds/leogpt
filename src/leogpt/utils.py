import json
import requests
import os

def as_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def as_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()    

def send_pushover_notification(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )