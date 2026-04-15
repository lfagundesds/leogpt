from pywa import WhatsApp

# Initialize client
#TODO: Generate access token automatically
wa = WhatsApp(
    phone_id="1079617868566833",
    token="EAAeY85obdToBRF3DiZAJPn8l7FlVahvfJBllHZAmPCsG4C0QCxAsjWlXInvZBBkvmz1htceErZAWGd42heUGeGFSKiQvXjkaHDEOJjei2fiXehnl0yZCr096fzG22HjAF89T2BMVn1peUnJ2t7ulOaOCyt2Jw0OrOGFEEbrRYIS7yM6bN5yl7MB6Qhoj8Kqv2ZAXozPoHD4Ux4dT4KD8nH1EZCUv29jEGImF8kSi8LdSSXlPL8iA61bm731Al97skVg3JxWZCrccZCnK14BtYjvziyWTMdHwxtpDC6d9omAZDZD"
)
print("Sending msg")
# Send a message

def send_message(text):
    try:
        wa.send_message(
            to="14159006023",
            text=text
        )
        print("msg sent")
    except Exception as e:
        print(f"Error: {e}")