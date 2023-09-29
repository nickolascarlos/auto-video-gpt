from moviepy.editor import CompositeVideoClip
from vidgear.gears import WriteGear
import numpy as np
import cv2

class VideoMaker:

    def __init__(self, coordinator, dimension, wh_ratio, fps):
        if dimension[0] == 'w':
            width = dimension[1]
            self.width = int(width)
            self.height = int(width*(1/wh_ratio))
        elif dimension[0] == 'h':
            height = dimension[1]
            self.width = int(height * wh_ratio)
            self.height = int(height)
        else:
            raise 'Use (d, v) where d is either "w" or "h" and v is the dimension size'

        self.wh_ratio = wh_ratio,
        self.fps = fps

        # Configures video coordinator
        if coordinator is not None:
            self.set_background_maker(coordinator.make_background)
            self.set_content_maker(coordinator.make_content)
            self.set_watermark_maker(coordinator.make_watermark)

    def set_background_maker(self, background):
        self.background = background

    def set_content_maker(self, content):
        self.content = content
    
    def set_watermark_maker(self, watermark):
        self.watermark = watermark

    def make(self):
        return CompositeVideoClip([*self.background(self), *self.content(self), *self.watermark(self)])
    
    def save(self, path):
        # Define video parameters
        # output_params = {
        #     "filename": "random_square_video.mp4",  # Output filename
        #     "compression": None,
        #     "fps": 24,  # Frames per second
        #     "frame_shape": (self.width, self.height),  # Frame dimensions (width, height)
        # }

        baked_video = self.make()

        # Initialize the VidGear writer
        with WriteGear(output="random_square_video.mp4", compression_mode=True, logging=True, **{'-vcodec': 'libx264', '-b:v': '2000k'}) as writer:
            for frame in baked_video.iter_frames(fps=self.fps, dtype='uint8'):
                writer.write(cv2.cvtColor(frame, cv2.COLOR_RGBA2BGRA))
