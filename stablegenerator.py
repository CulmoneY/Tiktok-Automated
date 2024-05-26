"""
Applies subtitles onto input video using stable-ts library, a modification of OpenAI's whisper module.
"""

import stable_whisper
import ffmpeg
import os

input_video = ""
input_video_name = input_video.replace(".mp4", "")


def select_input(inputfile: str):
    """
    Prompts the user to enter the path to the video file.
    """
    global input_video, input_video_name
    input_video = inputfile
    input_video_name = input_video.replace(".mp4", "")
    input_video_name = input_video_name.replace("/", "")


def extract_audio() -> str:
    """
    Extracts the audio from the given video file.
    :return: The path to the extracted audio file
    """
    extracted_audio = f"audio-{input_video_name}.wav"
    stream = ffmpeg.input(input_video)
    stream = ffmpeg.output(stream, 'temp/' + extracted_audio)
    ffmpeg.run(stream, overwrite_output=True)
    return 'temp/' + extracted_audio


def transcribe(audio: str, segment_level: bool):
    """
    Transcribes the given audio file.
    """
    model = stable_whisper.load_model('base')
    result = model.transcribe(audio)
    result.to_srt_vtt(filepath='temp/subtitles.srt', segment_level=segment_level, word_level=True, tag=('<font color="#fce803">', '</font>'))


def run(input_path: str, segment_level: bool = True):
    """
    Main function to apply subtitles to a video.
    :param input_path:
    :return:
    """
    select_input(input_path)
    audio_path = extract_audio()
    transcribe(audio_path, segment_level)
    if os.path.isfile(audio_path):
        os.remove(audio_path)
    else:
        print('File does not exist.')
    subtitle_file = 'temp/subtitles.srt'
    os.system(f'ffmpeg -y -i {input_path} -vf "subtitles={subtitle_file}:force_style=\'FontName=Impact,MarginV=145,MarginH=0,Alignment=6,Fontsize=8\'" {input_path.replace(".mp4", "")}_subtitled.mp4')
    if os.path.isfile(subtitle_file):
        os.remove(subtitle_file)
    if os.path.isfile(input_path):
        os.remove(input_path)
