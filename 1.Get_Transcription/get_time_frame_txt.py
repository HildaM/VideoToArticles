import os
import whisper
import moviepy.editor as mp

# 步骤 1: 从视频文件中提取音频
def extract_audio(video_path, audio_path):
    if not os.path.exists(audio_path):  # 检查音频文件是否已存在
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
    else:
        print(f"Audio file {audio_path} already exists. Skipping extraction.")

# 步骤 2: 使用Whisper模型将音频转换为带时间戳的文本
def transcribe_audio(audio_path):
    model = whisper.load_model("large", device='cuda')  # 或选择其他模型大小
    result = model.transcribe(audio_path)  # 移除了 include_timestamps=True
    return result

# 步骤 3: 将转录文本保存到TXT文件，时间戳保留两位小数
def save_transcription_to_txt(transcription_result, txt_path):
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        for segment in transcription_result["segments"]:
            # 只保留2位小数
            start = round(segment['start'], 2)
            end = round(segment['end'], 2)
            txt_file.write(f"{start}-{end}: {segment['text']}\n")

# 主函数
def main():
    video_path = "Chinese_video.mp4"  # 视频文件路径
    audio_path = "extracted_audio.wav"  # 提取的音频文件将保存在此路径
    txt_path = "transcription.txt"  # 转录文本将保存在此路径

    # 提取音频
    extract_audio(video_path, audio_path)

    # 转换音频为文本
    transcription_result = transcribe_audio(audio_path)

    # 保存转录文本到TXT文件
    save_transcription_to_txt(transcription_result, txt_path)

    print(f"Transcription saved to {txt_path}")

if __name__ == "__main__":
    main()
