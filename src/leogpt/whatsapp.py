from pywa import WhatsApp
import os

wa = WhatsApp(
    phone_id = os.getenv("WHATSAPP_PHONE_ID"),
    token = os.getenv("WHATSAPP_TOKEN")
)

def send_message(sender, text):
    try:
        wa.send_message(
            to = sender,
            text=text
        )
    except Exception as e:
        print(f"Error: {e}")