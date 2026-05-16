import litellm

#Models
CLAUDE_SONNET_4_6 = "anthropic/claude-sonnet-4-6"
GEMINI_2_5_FLASH = "gemini/gemini-2.5-flash"
GPT_4_O_MINI = "gpt-4o-mini"

"""
Wrapper that uses litellm to call different models.
Added here in case other models require specific functions or configuration.
"""
class LLMClient():
    def __init__(self, model: str):
        self.model = model        

    def send_message(self, messages: list[dict], tools: list[dict] = [], response_format= None):
        return litellm.completion(model=self.model, messages=messages, response_format=response_format).choices[0]

def create_llm_client(model: str) -> LLMClient:
    return LLMClient(model=model)