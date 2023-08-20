import moviepy.editor as mp
import openai
import os
import re
from pydub import AudioSegment
import pandas as pd


def convert_mp4_to_mp3(video_path: str) -> str:
    """
    convert_mp4_to_mp3 creates a mp3 file from a mp4 clip and returns the path to the mp3 file
    """
    save_path = video_path[: video_path.rfind("/")]

    audio_clip_path = f"{save_path}/{os.urandom(16).hex()}.mp3"
    clip = mp.VideoFileClip(video_path, verbose=False)
    clip.audio.write_audiofile(audio_clip_path, verbose=False)
    return audio_clip_path


def transcription_mp3_to_text(mp3_path: str) -> list[pd.DataFrame]:
    """
    transcription_mp3_to_text transcribes a mp3 file to text using OpenAI's API
    """
    save_path = mp3_path[: mp3_path.rfind("/")]

    batch_in_milliseconds = 1000 * 60 * 10  # 1000 miliseconds * 60 seconds * 10 minutes
    start = 0
    end = batch_in_milliseconds
    total_transcript = []

    song = AudioSegment.from_mp3(mp3_path)
    while start < len(song):
        random_mp3_file_name = f"{save_path}/{os.urandom(16).hex()}.mp3"
        song[start:end].export(random_mp3_file_name, format="mp3")
        arq = open(random_mp3_file_name, "rb")
        transcript = openai.Audio.transcribe(
            file=arq,
            model="whisper-1",
            response_format="verbose_json",
            language="pt",
        )
        total_transcript += __format_transcript__(transcript["segments"], start / 1000)
        start += batch_in_milliseconds
        end += batch_in_milliseconds

    return pd.concat(
        [
            pd.DataFrame(
                data={
                    "text": [segment["text"]],
                    "start": [segment["start"]],
                    "end": [segment["end"]],
                }
            )
            for segment in total_transcript
        ],
        ignore_index=True,
    )


def __format_transcript__(
    segments: list[dict[str, str | float]], offset: int
) -> list[dict[str, list[any]]]:
    merge_every = 8
    res = []
    for i in range(0, len(segments), merge_every):
        upper_bound = (
            i + merge_every if i + merge_every < len(segments) else len(segments)
        )
        upper_bound = upper_bound - 1
        res.append(
            {
                "start": segments[i]["start"] + offset,
                "end": segments[upper_bound]["end"] + offset,
                "text": " ".join(
                    [segment["text"] for segment in segments[i:upper_bound]]
                ),
            }
        )
    return res


def parser_text(filePath: str) -> list[dict[str, str | float]]:
    """
    parser text to input format
    """

    arq = open(filePath, "rb")
    text = arq.read().decode("utf-8")
    paragraph_regex = re.compile(r".+\n")
    dfs = [
        pd.DataFrame(
            data={
                "text": [batch.group()],
                "start": [batch.start()],
                "end": [batch.end()],
            }
        )
        for batch in paragraph_regex.finditer(text)
    ]
    return remove_small_batches(pd.concat(dfs, ignore_index=True))

def remove_small_batches(df):
    texts = df['text']
    indexes_small_batches = [idx for idx, text in enumerate(texts) if len(text) > 20]
    return df.iloc[indexes_small_batches]