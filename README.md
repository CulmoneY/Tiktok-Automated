
# Tiktok Automated

Have you ever seen a movie split into 50 parts on TikTok and thought "holy shit, that's a lot of views!". No? Just me?

#### Tiktok Automated automatically splits a movie into parts, subtitles them, then uploads them to TikTok.




## Authors

- [@CulmoneY](https://github.com/CulmoneY)
- [@hemmatio](https://github.com/hemmatio)




## Required Libraries/Software
- subtitlegenerator
- moviepy
    - [imagemagick](https://imagemagick.org/index.php)
- ffmpeg
- whisper
  
imagemagick should be installed separately (not using pip). After installation, be sure to correctly set the path of 'IMAGEMAGICK_BINARY' under external_libraries/site-packages/moviepy/config_defaults.py to 'C:\Program Files\ImageMagick-versionnumber\magick.exe', or wherever your installation was made to.
