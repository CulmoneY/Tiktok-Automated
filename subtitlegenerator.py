
"""
This file is responsible for generating subtitles for a given video.
"""
import ffmpeg
import whisper
import os
import math

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


def transcribe(audio: str):
    """
    Transcribes the given audio file.
    :param audio: the path to the audio file
    :return: the language, and the list of segments
    """
    model = whisper.load_model("tiny.en")
    transcription = model.transcribe(audio)
    language = transcription['language']
    # print("Transcription Language", language)
    segments = list(transcription['segments'])
    return segments, language


# def clean_format(segments: list) -> list:
#     """
#     Cleans and formats the given segments.
#     :param segments:
#     :return:
#     """
#     formatted_segments = []
#     for segment in segments:
#         start = segment['start']
#         end = segment['end']
#         text = segment['text']
#         formatted_segment = (start, end, text)
#         formatted_segments.append(formatted_segment)
#     return formatted_segments

def format_time(seconds):
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"

    return formatted_time


def generate_subtitle_file(language, segments):
    subtitle_file = f"temp/sub-{input_video_name}.{language}.srt"
    text = ""
    for index, segment in enumerate(segments):
        segment_start = format_time(segment['start'])
        segment_end = format_time(segment['end'])
        text += f"{str(index + 1)} \n"
        text += f"{segment_start} --> {segment_end} \n"
        text += f"{segment['text']} \n"
        text += "\n"

    with open(subtitle_file, "w", encoding='utf-8') as f:
        f.write(text)
    return subtitle_file

def run(inputfile: str): # TODO: RENAME THIS
    select_input(inputfile)
    extracted_audio = extract_audio()
    segments, language = transcribe(audio=extracted_audio)
    if os.path.isfile(extracted_audio):
        os.remove(extracted_audio)
    else:
        print('File does not exist.')
    subtitle_file = generate_subtitle_file(language, segments)
    os.system(f'ffmpeg -y -i {inputfile} -vf "subtitles={subtitle_file}:force_style=\'MarginV=145,MarginH=0,Alignment=6,Fontsize=8\'" {inputfile.replace(".mp4", "")}_subtitled.mp4')
    if os.path.isfile(subtitle_file):
        os.remove(subtitle_file)
    if os.path.isfile(inputfile):
        os.remove(inputfile)
