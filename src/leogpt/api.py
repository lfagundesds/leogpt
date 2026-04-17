import json
import os
from typing import Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
from leogpt.whatsapp import send_message
from leogpt.chat import Me

api = FastAPI(title="LeoGPT")

me = Me()

@api.get("/webhook", response_class=PlainTextResponse)
async def verify_webhook(request: Request) -> str:
    verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN")
    if not verify_token:
        raise HTTPException(status_code=500, detail="Missing WHATSAPP_VERIFY_TOKEN")

    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode != "subscribe" or not challenge:
        raise HTTPException(status_code=400, detail="Invalid verification params")
    if token != verify_token:
        raise HTTPException(status_code=403, detail="Invalid verify token")

    return challenge

@api.post("/webhook")
async def webhook(request: Request) -> dict[str, Any]:
    raw = await request.body()

    try:
        payload = json.loads(raw)

        sender, message = get_message_data(payload)

        response = me.chat(message, [])

        send_message(sender, response)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Body must be valid JSON") from exc
    return {"ok": True, "received": payload}

def get_message_data(payload: dict[str, Any]):
    try:
        message = payload["entry"][0]["changes"][0]["value"]["messages"][0]
        return message["from"], message["text"]["body"]
    except (KeyError, IndexError, TypeError) as exc:
        raise HTTPException(status_code=400, detail="Invalid WhatsApp payload structure") from exc