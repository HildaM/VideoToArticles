import os
import whisper
import moviepy.editor as mp
import constant
from config import Config

# Step 1: Extract audio from the video file
def extract_audio(video_path):
    audio_path = constant.AUDIO_PATH
    if not os.path.exists(audio_path):
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
    else:
        print(f"Audio file {audio_path} already exists. Skipping extraction.")

# Step 2: Convert audio to timestamped text using the Whisper model
def transcribe_audio(model, device):
    if os.path.exists(constant.TIMEFRAME_FILE):
        print(f"TimeFrame file {constant.TIMEFRAME_FILE} already exists. Skipping extraction.")
        return constant.TIMEFRAME_FILE, True

    model = whisper.load_model(model, device=device)
    result = model.transcribe(constant.AUDIO_PATH)
    return result, False

# Step 3: Save the transcribed text to a TXT file, with timestamps rounded to two decimal places
def save_transcription_to_txt(transcription_result, txt_path):
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        for segment in transcription_result["segments"]:
            start = round(segment['start'], 2)
            end = round(segment['end'], 2)
            txt_file.write(f"{start}-{end}: {segment['text']}\n")


class TimeFrame:

    def __init__(self, video_path: str, config: Config):
        self.video_path = video_path
        self._config = config

    def process(self):
        extract_audio(self.video_path)
        transcription_result, exist = transcribe_audio(self._config.whisper_model, self._config.device)

        if not exist:
            save_transcription_to_txt(transcription_result, constant.TIMEFRAME_FILE)
        return transcription_result