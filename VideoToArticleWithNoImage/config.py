from dotenv import load_dotenv
import os
from constant import *

class Config:
    def __init__(self):
        load_dotenv('.env')

        self.device = os.getenv(DEVICE)

        self.openai_api_base = os.getenv(OPENAI_API_BASE)
        self.openai_api_key = os.getenv(OPENAI_API_KEY)
        self.openai_model_name = os.getenv(OPENAI_MODEL_NAME)

        self.whisper_model = os.getenv(WHISPER_MODEL)