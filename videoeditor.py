"""
Video Editor

This module is responsible for processing movie clips. It segments a given movie clip into parts,
each lasting 61 seconds. Each clip is then enhanced with subtitles and a part number.
A watermark is also added to each clip. The processed clips are saved as mp4 files in a specified folder.

"""
import math
import random

import PIL
from subtitlegenerator import run
from moviepy.editor import *
import os


def os_concatenate(clip1_path: str, clip2_path: str):
    """
    acts like concatenate_clips but uses os.system to call ffmpeg to concatenate the clips
    :param clip1_path:
    :param clip2_path:
    :return:
    """
    t = 61
    # create a black background
    background = ColorClip(size=(1080, 192), color=(0, 0, 0), duration=t)
    # export to a temp file
    background.write_videofile("temp/temp.mp4", fps=1)
    # rescale the clips
    os.system(f"ffmpeg -y -i {clip1_path} -vf scale=1080:768 temp/clip1_rescaled.mp4")
    os.system(f"ffmpeg -y -i {clip2_path} -vf scale=1080:768 temp/clip2_rescaled.mp4")
    # concatenate the clips
    directory = os.path.dirname(os.path.realpath("videoeditor.py"))
    os.system(f"cd /d {directory}")
    os.system(f"ffmpeg -y -i temp/temp.mp4 -i temp/clip1_rescaled.mp4 -i temp/clip2_rescaled.mp4 -i temp/temp.mp4 -filter_complex vstack=inputs=4 output.mp4")


def concatenate_clips(clip1_path: str, clip2_path: str):
    """Combines two clips together. Temp variable names. CXhange later
    - preconditions:
        - duration of clip2 is at least duration of clip1
    """
    n = 61
    clip1 = VideoFileClip(clip1_path)
    clip2 = VideoFileClip(clip2_path)
    background1 = ColorClip(size=(1080, 192), color=(0,0,0), duration=n)
    background2 = ColorClip(size=(1080, 192), color=(0,0,0), duration=n)

    # resizing clip1 to be 1366 X 768
    clip1 = clip1.resize((1366, 768))
    clip2 = clip2.resize((1366, 768))

    clip1 = clip1.crop(x1=143, y1=0, x2=1223, y2=768)
    clip2 = clip2.crop(x1=143, y1=0, x2=1223, y2=768)

    final_clip = clips_array([[background1], [clip1], [clip2], [background2]])
    final_clip.write_videofile("my_stack2.mp4", fps=30)


def movie_splitter(filename: str):
    """Spilts the given video into multiple 61 second parts. Each clip is labeled with its respective part number.

    Args:
    video: The path to the MP4 video file
    """
    video = VideoFileClip(filename)
    print("Video Duration: ", video.duration)
    num_parts = math.ceil(video.duration / 61)
    print(num_parts)

    # Get the subtitles
    video = CompositeVideoClip([video] + subtitles(run(filename)))

    for part in range(1, num_parts):
        # Make the part text
        txt_clip = (TextClip(f"Part {part}", fontsize=20, color='black', bg_color='white')
                    .set_position(('center', 0.1), relative=True).set_duration(10))
        video_part = video.subclip(61 * (part - 1), 61 * part)
        result = CompositeVideoClip([video_part, txt_clip])
        result.write_videofile(f"part_{part}.mp4")

    # for the remaining portion of the video
    final_duration = min(10, video.duration - 61 * (num_parts - 1))
    txt_clip = (TextClip(f"Final", fontsize=20, color='black', bg_color='white')
                .set_position(('center', 0.1), relative=True).set_duration(final_duration)) # for subtitles, this should be a list of TextClips
    video_part = video.subclip(61 * (num_parts - 1))

    result = CompositeVideoClip([video_part, txt_clip])
    result.set_duration(video_part.duration).write_videofile(f"part_{num_parts}.mp4")


def get_brainrot(duration: float) -> VideoFileClip:
    """Returns a tiktok brainrot complilation the exact same duration as the specified value. Each 61 second segments will be a different
    random segment
    The videos within brainrot are labelled in sequential order {ex: 1, 2, 3 ...}
    """
    # How many files are in brainrot
    directory = 'brainrot/'
    entries = os.listdir(directory)
    file_count = sum(1 for entry in entries if os.path.isfile(os.path.join(directory, entry)))
    print(f"Number of files in '{directory}': {file_count}")

    # Select the random video
    video_name = f'brainrot/{random.randint(1, file_count)}'


def get_61segment(video: VideoFileClip) -> VideoFileClip:
    """Acts as a helper function to get_brainrot, and returns a 61-second segment of the given video"""
    maximimum_start = int((video.duration % 61) - 61)
    starttime = random.random




def subtitles(captions: list) -> list:
    """Processes each caption from captions and converts them into a txt_clip"""
    text_clips = []
    for caption in captions:
        start_time, end_time, text = caption
        txt_clip = TextClip(text, fontsize=24, color='white')
        txt_clip = txt_clip.set_start(start_time).set_duration(end_time - start_time).set_position('center')
        text_clips.append(txt_clip)
    return text_clips
