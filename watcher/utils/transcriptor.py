import moviepy.editor as mp
import openai
import os
from pydub import AudioSegment


def __format_transcript__(segments):
    return [
        {"start": segment["start"], "end": segment["end"], "text": segment["text"]}
        for segment in segments
    ]


def convert_mp4_to_mp3(video_path, save_path):
    clip = mp.VideoFileClip(video_path).subclip()
    clip.audio.write_audiofile(f"{save_path}/converted_audio.mp3")
    return "converted_audio.mp3"


def transcription_mp3_to_text(mp3_path, save_path):
    batch_in_minutes = 1000 * 60 * 10  # 1000 miliseconds * 60 seconds * 10 minutes
    start = 0
    end = batch_in_minutes
    total_transcript = []

    song = AudioSegment.from_mp3(f"{save_path}/{mp3_path}")
    while start < len(song):
        random_mp3_file_name = f"{save_path}/{os.urandom(16).hex()}.mp3"
        song[start:end].export(random_mp3_file_name, format="mp3")
        arq = open(random_mp3_file_name, "rb")
        transcript = openai.Audio.transcribe(
            file=arq, model="whisper-1", response_format="verbose_json", language="pt"
        )
        total_transcript += __format_transcript__(transcript["segments"])
        start += batch_in_minutes
        end += batch_in_minutes

    return total_transcript


video_path = "../../../sol.mp4"
save_path = "../../../temp"
path = f"{save_path}/{video_path}"

mp3_path = convert_mp4_to_mp3(video_path, save_path)
total_transcript = transcription_mp3_to_text(mp3_path, save_path)

print(total_transcript)
