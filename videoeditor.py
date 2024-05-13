"""
Video Editor

This module is responsible for processing movie clips. It segments a given movie clip into parts,
each lasting 61 seconds. Each clip is then enhanced with subtitles and a part number.
A watermark is also added to each clip. The processed clips are saved as mp4 files in a specified folder.

"""
import math
import PIL
from subtitlegenerator import run
from moviepy.editor import *


def concatenate_clips(clip1_path: str, clip2_path: str):
    """Combines two clips together. Temp variable names. CXhange later"""
    clip1 = VideoFileClip(clip1_path).resize(0.6)
    clip2 = VideoFileClip(clip2_path)
    center_x1, center_y1 = clip1.w / 2, clip1.h / 2
    center_x2, center_y2 = clip2.w / 2, clip2.h / 2
    crop_x1, crop_y1 = center_x1 - 1080 / 2, center_y1 - 1920 / 2
    crop_x2, crop_y2 = center_x2 - 1080 / 2, center_y2 - 1920 / 2
    clip1 = clip1.crop(width=1080)
    clip2 = clip2.crop(x1=crop_x2, y1=crop_y2, width=1080, height=(1920 - clip1.h))
    final_clip = clips_array([[clip1], [clip2]])
    final_clip.resize((1080, 1920)).write_videofile("my_stack.mp4")


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


def subtitles(captions: list) -> list:
    """Processes each caption from captions and converts them into a txt_clip"""
    text_clips = []
    for caption in captions:
        start_time, end_time, text = caption
        txt_clip = TextClip(text, fontsize=24, color='white')
        txt_clip = txt_clip.set_start(start_time).set_duration(end_time - start_time).set_position('center')
        text_clips.append(txt_clip)
    return text_clips
