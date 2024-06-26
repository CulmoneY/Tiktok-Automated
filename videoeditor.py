"""
Video Editor

This module is responsible for processing movie clips. It segments a given movie clip into parts,
each lasting 61 seconds. Each clip is then enhanced with subtitles and a part number.
A watermark is also added to each clip. The processed clips are saved as mp4 files in a specified folder.

"""
import math
import random
import subprocess
from stablegenerator import run
# from subtitlegenerator import run
from moviepy.editor import *
import os

time_segment = 180


def os_concatenate(clip1_path: str, clip2_path: str, part: int, duration: float = time_segment):
    """
    acts like concatenate_clips but uses os.system to call ffmpeg to concatenate the clips
    :param clip1_path:
    :param clip2_path:
    :return:
    """
    # create a black background
    background = ColorClip(size=(1080, 192), color=(0, 0, 0), duration=duration)
    # export to a temp file
    background.write_videofile("temp/temp.mp4", fps=1)
    # rescale and crop the clips
    os.system(f"ffmpeg -y -i {clip1_path} -vf scale=1366:768,crop=1080:768:143:0 -codec:a copy -r 30 temp/clip1_cropped.mp4")
    os.system(f"ffmpeg -y -i {clip2_path} -vf scale=1366:768,crop=1080:768:143:0 -codec:a copy -r 30 temp/clip2_cropped.mp4")
    # concatenate the clips
    os.system(f'ffmpeg -y -i temp/temp.mp4 -i temp/clip1_cropped.mp4 -i temp/clip2_cropped.mp4 -i temp/temp.mp4 '
              f'-filter_complex "[0:v][1:v]vstack=inputs=4[v]" -map "[v]" -map 1:a -codec:a copy -r 30 outputs/output{part}.mp4')
    # clean up temp files
    if os.path.isfile("temp/temp.mp4") and os.path.isfile("temp/clip1_cropped.mp4") and os.path.isfile("temp/clip2_cropped.mp4"):
        os.remove("temp/temp.mp4")
        os.remove("temp/clip1_cropped.mp4")
        os.remove("temp/clip2_cropped.mp4")
    run(f'outputs/output{part}.mp4', True)


def os_movie_splitter(movie_path: str):
    """
    splits the movie into time_segment second parts
    :param movie_path:
    :return:
    """
    command = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {movie_path}'
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    duration = float(process.stdout.strip())

    # Get Font Size
    command = f"ffprobe -v error -select_streams v:0 -show_entries stream=width -of default=nw=1:nk=1 {movie_path}"
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             universal_newlines=True)
    resolution = float(process.stdout.strip())
    font_size = math.ceil(resolution / 16)


    num_parts = math.ceil(duration / time_segment)
    for part in range(1, num_parts):
        # spilt into the 61-second segment
        start = format_time(time_segment * (part - 1))
        length = format_time(time_segment)
        os.system(f'ffmpeg -y -ss {start} -i {movie_path} -t {length} -map 0 -r 30 temp/temppart_{part}.mp4')

        command = (
            f'ffmpeg -y -i temp/temppart_{part}.mp4 -vf '
            f'"drawtext=fontfile=fonts/built_titling.otf:text=\'Part {part}\':'
            f'fontcolor=white:fontsize={font_size}:box=1:boxcolor=black@0.5:boxborderw=5:'
            f'x=(w-text_w)/2:y=30:enable=\'between(t,0,5)\'" -codec:a copy -r 30 temp/part_{part}.mp4'
        )
        os.system(command)
        if os.path.isfile(f'temp/temppart_{part}.mp4'):
            os.remove(f'temp/temppart_{part}.mp4')

        # Get the Parkour Video
        get_brainrot(time_segment, part)

        # Concatenate
        os_concatenate(f'temp/part_{part}.mp4', f'temp/brainrot{part}.mp4', part)
        if os.path.isfile(f'temp/part_{part}.mp4') and os.path.isfile(f'temp/brainrot{part}.mp4'):
            os.remove(f'temp/part_{part}.mp4')
            os.remove(f'temp/brainrot{part}.mp4')

    # for the remaining portion of the video
    final_start = format_time(time_segment * (num_parts - 1))
    final_duration = format_time(duration - (time_segment * (num_parts - 1)))
    os.system(f'ffmpeg -y -ss {final_start} -i {movie_path} -t {final_duration} -map 0 -r 30 temp/temppart_{num_parts}.mp4')

    command = (
        f'ffmpeg -y -i temp/temppart_{num_parts}.mp4 -vf '
        f'"drawtext=fontfile=fonts/built_titling.otf:text=\'Final\':'
        f'fontcolor=white:fontsize={font_size}:box=1:boxcolor=black@0.5:boxborderw=5:'
        f'x=(w-text_w)/2:y=30:enable=\'between(t,0,5)\'" -codec:a copy -r 30 temp/part_{num_parts}.mp4'
    )
    os.system(command)
    if os.path.isfile(f'temp/temppart_{num_parts}.mp4'):
        os.remove(f'temp/temppart_{num_parts}.mp4')

    # Get the Parkour Video
    get_brainrot(duration - (time_segment * (num_parts - 1)), num_parts)

    # Concatenate
    os_concatenate(f'temp/part_{num_parts}.mp4', f'temp/brainrot{num_parts}.mp4', num_parts, duration - (time_segment * (num_parts - 1)))
    if os.path.isfile(f'temp/part_{num_parts}.mp4') and os.path.isfile(f'temp/brainrot{num_parts}.mp4'):
        os.remove(f'temp/part_{num_parts}.mp4')
        os.remove(f'temp/brainrot{num_parts}.mp4')


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


def get_brainrot(duration: float, part: int):
    """Returns a tiktok brainrot complilation the exact same duration as the specified value. Each 61 second segments will be a different
    random segment.
    The videos within brainrot are labelled in sequential order {ex: brainrot_1, brainrot_2, brainrot_3 ...}
    Preconditions:
        - 0 < duration <= 61
        - brainrot clips do not contain any spaces in their names
    """
    # # How many files are in brainrot
    directory = 'brainrot/'
    entries = os.listdir(directory)
    # Define a tuple of video file extensions
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv')
    file_count = sum(
        1 for entry in entries if entry.endswith(video_extensions) and os.path.isfile(os.path.join(directory, entry)))
    duration = min(duration, time_segment)

    # Create dictionary mapping of all files in brainrot folder
    videos = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith(video_extensions)]
    videos = {i: f for i, f in enumerate(videos)}
    video_path = 'brainrot/' + videos[random.randint(0, file_count - 1)]
    get_61segment(video_path, part, duration)


def get_61segment(video_path: str, part: int, duration: float):
    """Acts as a helper function to get_brainrot, and returns a 61-second segment of the given video"""
    command = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {video_path}'
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             universal_newlines=True)
    duration_video = float(process.stdout.strip())
    maximimum_start = format_time(int(duration_video - duration))
    starttime = format_time(random.randrange(0, int(duration_video - duration)))
    duration = format_time(duration)
    os.system(f'ffmpeg -y -ss {starttime} -i {video_path} -t {duration} -map 0 -codec:v copy -an -r 30 temp/brainrot{part}.mp4')


def subtitles(captions: list) -> list:
    """Processes each caption from captions and converts them into a txt_clip"""
    text_clips = []
    for caption in captions:
        start_time, end_time, text = caption
        txt_clip = TextClip(text, fontsize=24, color='white')
        txt_clip = txt_clip.set_start(start_time).set_duration(end_time - start_time).set_position('center')
        text_clips.append(txt_clip)
    return text_clips

def main():
    videopath = input("Enter the path of the video: ")
    os_movie_splitter(videopath)

if __name__ == "__main__":
    main()
