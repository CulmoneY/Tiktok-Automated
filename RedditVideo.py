import math
import random
from texttospeech import tts
import os
import subprocess

text = "I woke up to a blinking notification on my phone: one unread message from my dad. It was strange since he had passed away over a year ago."


def story_maker(title: str, text: str):
    """"""
    duration, title_duration = 0, 0
    tts(title, 'temp/titletts')
    tts(text, 'temp/texttts')
    if os.path.isfile("temp/titletts.mp3") and os.path.isfile("temp/texttts.mp3"):
        command = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 temp/titletts.mp3'
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 universal_newlines=True)
        title_duration = float(process.stdout.strip())

        command = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 temp/texttts.mp3'
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 universal_newlines=True)
        duration = float(
            process.stdout.strip()) + title_duration + 1  # The plus 1 is for a space between the title and video itself

    get_background(duration)
    import_title(title, title_duration)
    add_audio(title_duration)


def add_audio(title_duration):
    """Adds the audio to the current titled background.
    The First audio plays instantly, the second plays 1 second later"""
    os.system("ffmpeg -y -i temp/titlefinal.mp4 -i temp/titletts.mp3 -map 0:v "
              "-map 1:a -c:v copy -c:a aac -strict experimental temp/intermediate_video.mp4")
    os.system(f"ffmpeg -y -i temp/intermediate_video.mp4 -i temp/texttts.mp3 -filter_complex"
              f" \"[1:a]adelay={title_duration + 1}s|{title_duration + 1}"
              f"s[a2]; [0:a][a2]amix=inputs=2:duration=longest[a]\" "
              f"-map 0:v -map \"[a]\" -c:v copy -c:a aac -strict experimental temp/audiovideo.mp4")
    #TODO: Remove the temp audio files, aswell the temp titlefinal


def expand_text(text: str) -> str:
    """Rewrites the given text to expand the acronyms
    For example TIL = Today I Learned"""
    pass


def import_title(title: str, title_duration: float):
    """Adds a title screen to the given background on the correct portion of the video. Correctly
    formats the name of the title to fit within the specified image"""
    if not os.path.isfile("temp/background.mp4"):
        pass
    os.system(
        f"ffmpeg -y -i temp/background.mp4 -i videos/title.png -filter_complex [0][1]overlay=x=(main_w-overlay_w)/2:y=(main_h-overlay_h)/2:enable=\'between(t,0,{title_duration})\' -r 30 temp/title.mp4")

    # Add the text
    #TODO: Delete background file
    title1, title2, title3, = format_text(title)
    command = (
        f'ffmpeg -y -i temp/title.mp4 -vf '
        f'"drawtext=fontfile=fonts/built_titling.otf:text=\'{title1}\':'
        f'fontcolor=black:fontsize=30:'
        f'x=w/2 - 245:y=h/2 - 30:enable=\'between(t,0,{title_duration})\'",'  # End of Text 1
        f'"drawtext=fontfile=fonts/built_titling.otf:text=\'{title2}\':'
        f'fontcolor=black:fontsize=30:'
        f'x=w/2 - 245:y=h/2 + 5 :enable=\'between(t,0,{title_duration})\'",'  # End of Text 2
        f'"drawtext=fontfile=fonts/built_titling.otf:text=\'{title3}\':'
        f'fontcolor=black:fontsize=30:'
        f'x=w/2 - 245:y=h/2 + 40:enable=\'between(t,0,{title_duration})\'" -codec:a copy -r 30 temp/titlefinal.mp4'
    )
    os.system(command)
    if os.path.isfile('temp/title.mp4'):
        os.remove('temp/title.mp4')


def format_text(title: str) -> tuple:
    """Acts as a helper function to import_title, spilting the longer title into 3 seperate parts
    preconditions:
        len(title) <= 300
    """
    words = title.split()
    lines = {1: '', 2: '', 3: ''}
    characters, curr_word = 0, 1

    for word in words:
        if characters + len(word) + 1 > 57:  # Check if adding this word exceeds line limit
            curr_word += 1
            if curr_word > 3:  # Limit to three lines
                lines[curr_word - 1] += '...'
                break
            characters = 0  # Reset characters count for new line

        lines[curr_word] += word + ' '
        characters += len(word) + 1

    # Return tuple of all four lines, ensuring each index is used
    return (lines[1].rstrip(), lines[2].rstrip(), lines[3].rstrip())


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
    os.system(
        f'ffmpeg -y -ss {starttime} -t {duration} -i {video_path} -map 0 -codec:v copy -an -r 30 temp/background.mp4')


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
