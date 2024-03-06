import os
import whisper
import moviepy.editor as mp
import constant

# 步骤 1: 从视频文件中提取音频
def extract_audio(video_path, audio_path):
    if not os.path.exists(audio_path):  # 检查音频文件是否已存在
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
    else:
        print(f"Audio file {audio_path} already exists. Skipping extraction.")

# 步骤 2: 使用Whisper模型将音频转换为带时间戳的文本
def transcribe_audio(audio_path):
    if os.path.exists(constant.TIMEFRAME_FILE):
        print(f"TimeFrame file {constant.TIMEFRAME_FILE} already exists. Skipping extraction.")
        return constant.TIMEFRAME_FILE, True

    model = whisper.load_model("large", device='cuda')  # 或选择其他模型大小
    result = model.transcribe(audio_path)  # 移除了 include_timestamps=True,默认携带时间戳
    return result, False

# 步骤 3: 将转录文本保存到TXT文件，时间戳保留两位小数
def save_transcription_to_txt(transcription_result, txt_path):
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        for segment in transcription_result["segments"]:
            # 只保留2位小数
            start = round(segment['start'], 2)
            end = round(segment['end'], 2)
            txt_file.write(f"{start}-{end}: {segment['text']}\n")


class TimeFrame:

    def __init__(self, video_path: str):
        self.video_path = video_path

    def process(self):
        audio_path = constant.AUDIO_PATH  # 提取的音频文件将保存在此路径
        timeframe_path = constant.TIMEFRAME_FILE  # 转录文本将保存在此路径

        # 提取音频
        extract_audio(self.video_path, audio_path)

        # 转换音频为文本
        transcription_result, exist = transcribe_audio(audio_path)

        # 保存转录文本到TXT文件
        if not exist:
            save_transcription_to_txt(transcription_result, timeframe_path)
        return transcription_result