from moviepy.editor import CompositeVideoClip

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
        self.make().write_videofile(path, fps=self.fps, threads=4)
