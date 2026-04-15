import json
from typing import Any
import gradio as gr
from fastapi import FastAPI, HTTPException, Request
from leogpt.chat import build_chat_interface
from leogpt.whatsapp import send_message
from leogpt.chat import Me

api = FastAPI(title="LeoGPT")

me = Me()


@api.post("/webhook")
async def webhook(request: Request) -> dict[str, Any]:
    raw = await request.body()
    if not raw.strip():
        return {"ok": True}
    try:
        payload = json.loads(raw)
        print(f"payload: {payload}")

        #TODO: Make it async
        response = me.chat(payload["message"], [])

        send_message(response)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="Body must be valid JSON") from exc
    return {"ok": True, "received": payload}

app = gr.mount_gradio_app(api, build_chat_interface(), path="/")
