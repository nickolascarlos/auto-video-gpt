from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})

from ContentFactory import *
from arguments_parsing import get_arguments
from coordinators import get_coordinator_class_by_name
from video_creation import create_video

if __name__ == '__main__':
    arguments = get_arguments()
    content_factory = GPTContentFactory(arguments['api_key'])
    video_coordinator_class = get_coordinator_class_by_name(arguments['coordinator'])
    create_video(video_coordinator_class, arguments, content_factory)
