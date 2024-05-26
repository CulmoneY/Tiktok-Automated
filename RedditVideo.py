import math
import random
from texttospeech import tts
import os
import subprocess
text = ""

def story_maker(title: str, text: str):
    """"""
    duration = 0
    tts(title, 'temp/titletts')
    tts(text, 'temp/texttts')
    if os.path.isfile("temp/titletts") and os.path.isfile("temp/texttts"):
        command = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 temp/titletts'
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 universal_newlines=True)
        duration = float(process.stdout.strip()) + 1 #The plus 1 is for a space between the title and video itself

        command = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 temp/texttts'
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 universal_newlines=True)
        duration += float(process.stdout.strip())
    get_background(duration)


def get_background(duration: float):
    """Creates relaxing background footage the same duration as the specified value."""
    # # How many files are in background
    directory = 'background/'
    entries = os.listdir(directory)
    # Define a tuple of video file extensions
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv')
    file_count = sum(
        1 for entry in entries if entry.endswith(video_extensions) and os.path.isfile(os.path.join(directory, entry)))

    # Create dictionary mapping of all files in brainrot folder
    videos = [f for f in os.listdir(directory) if
              os.path.isfile(os.path.join(directory, f)) and f.endswith(video_extensions)]
    videos = {i: f for i, f in enumerate(videos)}
    video_path = directory + videos[random.randint(0, file_count - 1)]

    # Pull the duration of the video
    command = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {video_path}'
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             universal_newlines=True)
    duration_video = float(process.stdout.strip())
    starttime = format_time(random.randrange(0, int(duration_video - duration)))
    duration = format_time(duration)
    os.system(f'ffmpeg -y -ss {starttime} -t {duration} -i {video_path} -map 0 -codec:v copy -an -r 30 temp/background.mp4')

def format_time(seconds: float) -> str:
    """Converts the time from decimal format to sexagecimal format:
        HH:MM:SS.MS
    """

    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d}.{milliseconds:03d}"

    return formatted_time
