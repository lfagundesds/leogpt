import gradio as gr
from dotenv import load_dotenv
from pydantic import BaseModel
from leogpt.llm_clients import create_llm_client, GPT_OSS_120_B, GPT_4_O_MINI
from leogpt.tools import tools, handle_tool_call
from leogpt.prompts import response_provider_system_prompt, evaluator_system_prompt, evaluator_user_prompt, response_provider_rerun_prompt
from leogpt.utils import as_text, send_pushover_notification

load_dotenv(override=True)

#Important variables
name = "Leo Fagundes"
response_provider = create_llm_client(GPT_4_O_MINI)
evaluator = create_llm_client(GPT_OSS_120_B)

class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str

class Me:
    def __init__(self, should_evaluate = False):
        self.name = name
        self.summary = as_text("files/summary.txt")
        self.resume = as_text("files/resume.txt")
        self.should_evaluate = should_evaluate
    
    def evaluate(self, reply, message, history) -> Evaluation:
        messages = [{"role": "system", "content": evaluator_system_prompt(self.name, self.resume, self.summary)}] + [{"role": "user", "content": evaluator_user_prompt(reply, message, history)}]
        response = evaluator.send_message(messages=messages, response_format=Evaluation)
        return response.message.parsed
    
    def chat(self, message, history):
        done = False
        system_prompt = response_provider_system_prompt(self.name, self.summary, self.resume)
        messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]

        try:
            while not done:
                response = response_provider.send_message(messages=messages, tools=tools)
                if response.finish_reason=="tool_calls":
                    message = response.message
                    tool_calls = message.tool_calls
                    results = handle_tool_call(tool_calls)
                    messages.append(message)
                    messages.extend(results)            
                elif self.should_evaluate:      
                    reply = response.message.content          
                    evaluation = self.evaluate(reply, message, history)
                    if evaluation.is_acceptable:
                        done = True
                    else:
                        messages = [{"role": "system", "content": response_provider_rerun_prompt(system_prompt, reply, evaluation.feedback)}] + history + [{"role": "user", "content": message}]
                else:
                    done = True
            return response.message.content
        except Exception as e:
            send_pushover_notification(f"Internal Error: {e}")
            return f"Sorry, I've encountered an internal issue and will be working on solving it as soon as possible."

def build_chat_interface() -> gr.ChatInterface:
    me = Me()
    return gr.ChatInterface(me.chat)