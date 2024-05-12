"""
Video Editor

This module is responsible for processing movie clips. It segments a given movie clip into parts,
each lasting 61 seconds. Each clip is then enhanced with subtitles and a part number.
A watermark is also added to each clip. The processed clips are saved as mp4 files in a specified folder.

"""
from typing import IO
from moviepy.editor import *

def movie_spilter(filename: str):
    """Spilts the given video into multiple 61 second part. Each clip is enchanced with a part number, and save as a temp. mp4 file

    Args:
    video: The path fto the MP4 video file
    """
    video = VideoFileClip(filename)
    num_parts = video.duration() // 61
    for part in range(1, num_parts + 1):
        # Make the part text
        txt_clip = (TextClip(f"Part {part}", fontsize = 40, color = 'white', bg_color = 'red')
                    .set_position('North').set_duration(10))
        video_part = video.subclip(61 * (part - 1), 61 * part)
        result = CompositeVideoClip([video_part, txt_clip])

        video.ipython_display()


