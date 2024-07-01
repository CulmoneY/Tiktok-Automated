import math
import random
from texttospeech import tts
import os
import subprocess
from stablegenerator import run
from storyscraper import gather_n_stories
import re

text = "My fiancee (28f) and I (29m) are getting married in a couple of months. We both lost our moms. While my fiancee was raised by her grandparents, I was raised by dad and later my stepmother, his second wife. So while my fiancee has no drama about wanting to display a photo of her late mom. There is some about me displaying my mom. My siblings get why I want to do it. But my stepmother and stepsiblings do not. They feel her late husband/their late dad and their late child/sibling should also get photos displayed since they are also immediate family. But they're not my family, immediate or otherwise. Both of them had passed before my dad met his wife.My stepmother feels insecure that I don't just want to have photos of late family but of just my mom, she feels like it's a dig at her because I also don't call her my mom and I'm not close to her. My dad just wants his wife and stepkids happy. Stepkids feel like I should embrace \"all parts of the family but here and not here\" and they said if they did the photo thing, they'd include my mom with their dad.I made my stance clear and my answer was no. Which only brought more of the \"we're either a family or we're not\". My siblings stayed by my side and one of them was like well we're not an actual family so it's whatever, which only added fuel to the fire. I was then told I need to do this to restore family harmony and I should want to do this for my family. I told them I don't want to do this for them and I won't. They said it should be all three photos or none at all.AITA?"
title = "AITA for not agreeing to display a photo of my stepmothers late husband and child at my wedding?"

# TODO: Remove/reformat text to not contain quotation marks and colons

def make_n_stories():
    """
    Makes n stories from the Reddit API
    :return:
    """
    stories = gather_n_stories()  # this just makes a file, you need to read the file lol
    for n in range(len(stories)):
        story_maker(stories[n]['title'], stories[n]['text'], n)
    if os.path.isfile('temp/stories.json'):
        os.remove('temp/stories.json')


def story_maker(title: str, text: str, n: int = 0):
    """"""
    duration, title_duration = 0, 0
    tts(expand_text(title), 'temp/titletts')
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
    run('temp/audiovideo.mp4', segment_level=False, title_duration=title_duration+0.90, n=n)
    os.system(f"ffmpeg -y -i temp/audiovideo_subtitled{n}.mp4 -vf "
              f"crop=0.31640625*in_w:in_h:0.341796875*in_w:0 "
              f"-codec:a copy -r 30 stories/video{n}.mp4")
    # if os.path.isfile(f'temp/audiovideo_subtitled{n}.mp4'):
    #     os.remove(f'temp/audiovideo_subtitled{n}.mp4')
    if os.path.isfile('temp/audio-tempaudiovideo.wav'):
        os.remove('temp/audio-tempaudiovideo.wav')

def add_audio(title_duration):
    """Adds the audio to the current titled background.
    The First audio plays instantly, the second plays 1 second later"""
    # os.system("ffmpeg -y -i temp/titlefinal.mp4 -i temp/titletts.mp3 -map 0:v "
    #           "-map 1:a -c:v copy -c:a aac -strict experimental temp/intermediate_video.mp4")
    # os.system(f"ffmpeg -y -i temp/intermediate_video.mp4 -i temp/texttts.mp3 -filter_complex"
    #           f" \"[1:a]adelay={title_duration + 1}s|{title_duration + 1}"
    #           f"s[a2]; [0:a][a2]amix=inputs=2:duration=longest[a]\" "
    #           f"-map 0:v -map \"[a]\" -c:v copy -c:a aac -strict experimental temp/audiovideo.mp4")

    # Convert title_duration from seconds to milliseconds and add 1 second gap
    delay = int((title_duration + 1) * 1000)

    # Add the first audio file
    os.system("ffmpeg -y -i temp/titlefinal.mp4 -i temp/titletts.mp3 -map 0:v "
              "-map 1:a -c:v copy -c:a aac -strict experimental temp/intermediate_video_with_title_audio.mp4")

    # Add the second audio file with delay
    os.system(f"ffmpeg -y -i temp/intermediate_video_with_title_audio.mp4 -i temp/texttts.mp3 -filter_complex"
              f" \"[1:a]adelay={delay}|{delay}[a2]; [0:a][a2]amix=inputs=2:duration=longest[a]\" "
              f"-map 0:v -map \"[a]\" -c:v copy -c:a aac -strict experimental temp/audiovideo.mp4")

    # Clean up temp files
    if os.path.isfile('temp/titletts.mp3'):
        os.remove('temp/titletts.mp3')
    if os.path.isfile('temp/texttts.mp3'):
        os.remove('temp/texttts.mp3')
    if os.path.isfile('temp/intermediate_video_with_title_audio.mp4'):
        os.remove('temp/intermediate_video_with_title_audio.mp4')
    if os.path.isfile('temp/titlefinal.mp4'):
        os.remove('temp/titlefinal.mp4')

def expand_text(text):
    """Rewrites the given text to expand the acronyms
        For example TIL = Today I Learned"""
    acronyms = {
        'TIL': "Today I Learned",
        "AITA": "Am I the A-hole",
        "NTA": "Not the A-hole",
        "YTA": "You're the A-hole",
        "TIFU": "Today I effed up",
        "WIBTA": "Would I be the A-hole",
        "TA": "The A-hole"
    }

    pattern = re.compile(r'\b(' + '|'.join(re.escape(key) for key in acronyms.keys()) + r')\b')

    def replace(match):
        return acronyms[match.group(0)]

    return pattern.sub(replace, text)


def import_title(title: str, title_duration: float):
    """Adds a title screen to the given background on the correct portion of the video. Correctly
    formats the name of the title to fit within the specified image"""
    if not os.path.isfile("temp/background.mp4"):
        pass
    # Find the correct scale.
    command = 'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x temp/background.mp4'
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             universal_newlines=True)
    background_dimensions = process.stdout.strip()

    # Extract width and height from the output
    background_width, background_height = map(int, background_dimensions.split('x'))

    # Calculate the scaled dimensions
    scaled_width = int(background_width * 0.21171875)
    scaled_height = int(background_height * 0.17638888888)
    print(f"The width and height are: {background_width} and {background_height}")
    command = (
        f"ffmpeg -y -i temp/background.mp4 -i videos/title.png "
        f"-filter_complex "
        f"[1:v]scale={scaled_width}:{scaled_height}[scaled_overlay];"
        f"[0:v][scaled_overlay]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2:enable='between(t,0,{title_duration})' "
        f"-r 30 temp/title.mp4"
    )
    os.system(command)

    # Add the text
    if os.path.isfile('temp/background.mp4'):
        os.remove('temp/background.mp4')
    font_size = round(0.02083333333 * background_height)
    title1, title2, title3, = format_text(title)
    h1 = background_height/2 - 0.11811023622*scaled_height
    h2 = background_height/2 + 0.01968503937*scaled_height
    h3 = background_height/2 + 0.15748031496*scaled_height
    w = background_width/2 - 0.45202952029*scaled_width
    command = (
        f'ffmpeg -y -i temp/title.mp4 -vf '
        f'"drawtext=fontfile=fonts/built_titling.otf:text=\'{title1}\':'
        f'fontcolor=black:fontsize={font_size}:'
        f'x={w}:y={h1}:enable=\'between(t,0,{title_duration})\'",'  # End of Text 1
        f'"drawtext=fontfile=fonts/built_titling.otf:text=\'{title2}\':'
        f'fontcolor=black:fontsize={font_size}:'
        f'x={w}:y={h2}:enable=\'between(t,0,{title_duration})\'",'  # End of Text 2
        f'"drawtext=fontfile=fonts/built_titling.otf:text=\'{title3}\':'
        f'fontcolor=black:fontsize={font_size}:'
        f'x={w}:y={h3}:enable=\'between(t,0,{title_duration})\'" -codec:a copy -r 30 temp/titlefinal.mp4'
    )
    os.system(command)
    if os.path.isfile('temp/title.mp4'):
        os.remove('temp/title.mp4')


def format_text(title: str) -> tuple:
    """Acts as a helper function to import_title, spilting the longer title into 3 seperate parts
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
