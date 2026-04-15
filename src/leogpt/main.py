import uvicorn
import gradio as gr
from leogpt.chat import build_chat_interface
from leogpt.api import api

def main() -> None:
    app = gr.mount_gradio_app(api, build_chat_interface(), path="/")
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
