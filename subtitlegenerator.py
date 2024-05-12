
"""
This file is responsible for generating subtitles for a given video.
"""
import ffmpeg
import whisper
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


def transcribe(audio: str):
    """
    Transcribes the given audio file.
    :param audio: the path to the audio file
    :return: the language, and the list of segments
    """
    model = whisper.load_model("base")
    transcription = model.transcribe(audio)
    language = transcription['language']
    print("Transcription Language", language)
    segments = list(transcription['segments'])
    return segments


def clean_format(segments: list) -> list:
    """
    Cleans and formats the given segments.
    :param segments:
    :return:
    """
    formatted_segments = []
    for segment in segments:
        start = segment['start']
        end = segment['end']
        text = segment['text']
        formatted_segment = (start, end, text)
        formatted_segments.append(formatted_segment)
    return formatted_segments


def run(inputfile: str):
    select_input(inputfile)
    extracted_audio = extract_audio()
    segments = transcribe(audio=extracted_audio)
    if os.path.isfile(extracted_audio):
        os.remove(extracted_audio)
    else:
        print('File does not exist.')
    return clean_format(segments)

