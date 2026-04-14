from abc import ABC, abstractmethod
from openai import OpenAI
import os

DEEPSEEK_CHAT = "deepseek-chat"
GPT_4_O_MINI = "gpt-4o-mini"
GEMINI_2_5_FLASH = "gemini-2.5-flash"
GPT_OSS_120_B = "openai/gpt-oss-120b"

deepseek_models = [
    DEEPSEEK_CHAT
]

gemini_models = [
    GEMINI_2_5_FLASH
]

groq_models = [
    GPT_OSS_120_B
]

open_ai_models = [
    GPT_4_O_MINI
]

class LLMClient(ABC):
    @abstractmethod
    def send_message(self, messages: list[dict], tools: list[dict] = [], response_format= None):
        pass

class OpenAIClient(LLMClient):
    def __init__(self, model: str):
        self.model = model
        self.openai = OpenAI()

    def send_message(self, messages: list[dict], tools: list[dict] = [], response_format= None):
        if response_format:
            response = self.openai.beta.chat.completions.parse(model=self.model, messages=messages, response_format=response_format)
        else:
            response = self.openai.chat.completions.create(model=self.model, messages=messages, tools=tools)
        return response.choices[0]

class DeepseekClient(OpenAIClient):
    def __init__(self, model: str):
        super().__init__(model)        
        self.openai = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"), 
            base_url="https://api.deepseek.com"
        )

class GeminiClient(OpenAIClient):
    def __init__(self, model: str):
        super().__init__(model)        
        self.openai = OpenAI(
            api_key=os.getenv("GOOGLE_API_KEY"), 
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

class GroqClient(OpenAIClient):
    def __init__(self, model: str):
        super().__init__(model)        
        self.openai = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"), 
            base_url="https://api.groq.com/openai/v1"
        )

def create_llm_client(model: str) -> LLMClient:    
    if model in deepseek_models:
        return DeepseekClient(model=model)
    if model in gemini_models:
        return GeminiClient(model=model)
    if model in groq_models:
        return GroqClient(model=model)
    if model in open_ai_models:
        return OpenAIClient(model=model)
    raise Exception("An unknown model was received.")