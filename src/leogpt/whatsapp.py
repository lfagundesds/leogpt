from pywa import WhatsApp
import os

# Initialize client
#TODO: Generate access token automatically
wa = WhatsApp(
    phone_id = os.getenv("WHATSAPP_PHONE_ID"),
    token = os.getenv("WHATSAPP_TOKEN")
)

def send_message(text):
    try:
        wa.send_message(
            to = os.getenv("WHATSAPP_PHONE_NUMBER"),
            text=text
        )
        print("msg sent")
    except Exception as e:
        print(f"Error: {e}")