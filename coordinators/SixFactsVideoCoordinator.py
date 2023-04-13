from moviepy.editor import ColorClip, ImageClip, CompositeVideoClip, TextClip
from icrawler.builtin import GoogleImageCrawler
import json, random, os

# Coordinator for Youtube Shorts compatible
# videos that consist of six "slides" with
# white text and a zooming background image

class SixFactsVideoCoordinator:
    
    standardGPTPrompt = "Propose 6 detailed slides on \"{{SUBJECT}}\", with exactly one very informative sentence (do not include quotes in the sentence\", in JSON array format, in such a way that the title (maximum 5 words) of the slide occupy the name key \"title\" and the content occupy the name key \"content\". Also include in the JSON object, in the \"image\" key, a very simple and well-contextualized image description consistent with the content of each of the slides. Write only just the JSON object, don't write anything other than the JSON code!"
    
    def __init__(self, theme, content, title_font, content_font):
        self.theme = theme
        self.content = json.loads(content)
        self.title_font = title_font
        self.content_font = content_font

    def backgroundMaker(self, video_maker):
        background = ColorClip((video_maker.width, video_maker.height), (0,0,0)).set_duration(59)
        
        for i, f in enumerate(self.content):
            image = SixFactsVideoCoordinator.getRelatedImage(f['image']) # Returns an ImageClip
            image = image.resize(width=video_maker.width) if image.h > image.w else image.resize(height=video_maker.height)
            
            image = image.set_duration(9.8)\
                        .set_start(i*9.8)\
                        .set_pos(("center", "center"))
                        #.resize(lambda t: 1+(t/9.8)/6)\
            
            background = CompositeVideoClip([background, image])
        
        background = CompositeVideoClip([
                        background,
                        ColorClip((video_maker.width, video_maker.height), (0,0,0))\
                            .set_opacity(0.8)\
                            .set_duration(59)
                        ])
        return [background]
    
    def contentMaker(self, video_maker):
        slides = []
        for i, element in enumerate(self.content):
            title = TextClip(element['title'], 
                             fontsize=25, 
                             font=self.title_font, 
                             method='label', 
                             color='white')\
                    .set_duration(9.8)\
                    .set_start(i*9.8)\
                    .set_end((i+1)*9.8)\
                    .margin(top=50, opacity=0)\
                    .set_pos(("center", "top"))
            
            text = TextClip(element['content'], 
                            fontsize=37, 
                            font=self.content_font, 
                            method='caption', 
                            color='white', 
                            size=(video_maker.width - 100, 512), 
                            align='West')\
                    .margin(bottom=50, opacity=0)\
                    .set_duration(9.8)\
                    .set_start(i*9.8)\
                    .crossfadein(1)\
                    .set_end((i+1)*9.8)\
                    .set_pos(("center", "bottom"))
            
            timer = ColorClip((video_maker.width, video_maker.height), (255, 0, 0))\
                    .resize(lambda t: (10 + (video_maker.width - 10)*(t/9.8), 10))\
                    .set_duration(9.8)\
                    .set_start(i*9.8)\
                    .set_pos(("center", "top"))
            
            slides.extend([title, text, timer])

        return slides

    def watermarkMaker(self, video_maker):
      return []
    
    
    @staticmethod
    # Returns a random image, from Google Image, related to the query
    def getRelatedImage(query, temp_image_dir = './image_dir_temp/'):
        
        if not temp_image_dir.endswith('/'):
            temp_image_dir += '/'

        google_crawler = GoogleImageCrawler(parser_threads=4,
                                            downloader_threads=4,
                                            storage={'root_dir': temp_image_dir})
        
        google_crawler.crawl(keyword=query, offset=0, max_num=1,
                            min_size=(400, 400), max_size=None)
        
        chosen_image = random.choice([temp_image_dir + image_file for image_file in os.listdir(temp_image_dir)])
        image_clip = ImageClip(chosen_image)
        os.remove(chosen_image)

        return image_clip