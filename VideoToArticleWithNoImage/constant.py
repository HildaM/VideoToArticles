import os

# 全局变量
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TEMP_FOLDER = os.path.join(PROJECT_ROOT, "temp")
AUDIO_PATH = os.path.join(TEMP_FOLDER, "extracted_audio.wav")
TIMEFRAME_FILE = os.path.join(TEMP_FOLDER, "timeframe.txt")
TOPIC_BLOCK_TIMELINE = os.path.join(TEMP_FOLDER, "topic_timeline.txt")
RESULT_FOLDER = os.path.join(PROJECT_ROOT, "result")

# Config Key
DEVICE = "DEVICE"

## OpenAI
OPENAI_API_BASE = "OPENAI_API_BASE"
OPENAI_API_KEY = "OPENAI_API_KEY"
OPENAI_MODEL_NAME = "OPENAI_MODEL_NAME"

## whisper
WHISPER_MODEL = "WHISPER_MODEL"