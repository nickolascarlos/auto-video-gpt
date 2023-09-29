from moviepy.editor import ColorClip, ImageClip, CompositeVideoClip, TextClip
from icrawler.builtin import GoogleImageCrawler
import json, random, os

from effects import zoom_in_effect

# Coordinator for Youtube Shorts compatible
# videos that consist of six "slides" with
# white text and a zooming background image
class SixFactsVideoCoordinator:
    
    standardGPTPrompt = """Generate a JSON array containing 6 detailed slides on "{{SUBJECT}}". 

                        Each slide should have a title (up to 5 words) in the 'title' key and a descriptive sentence (without quotes) in the 'content' key.

                        Additionally, include a concise, contextually relevant image description in the 'image' key for each slide.

                        Important!!! Provide only the raw/pure JSON object as plain text, in such a way that it's possible to parse it directly from your response, so don't include any additional text or marks other than the JSON object.

                        Your answer must be a valid JSON object, such that I can parse it without any errors. So, no explanation and no comments, just and only the JSON object. Like this:

                        [ {
                            "title": "...",
                            "content": "...",
                            "image": "..."
                        }, ... ]"""
    
    def __init__(self, theme, content, title_font, content_font):
        self.theme = theme
        self.content = json.loads(content)
        self.title_font = title_font
        self.content_font = content_font

    def make_background(self, video_maker):
        background = ColorClip((video_maker.width, video_maker.height), (0,0,0)).set_duration(59)
        
        for i, f in enumerate(self.content):
            image = SixFactsVideoCoordinator.get_related_image(f['image']) # Returns an ImageClip
            image = image.resize(width=video_maker.width) if image.h > image.w else image.resize(height=video_maker.height)
            
            image = zoom_in_effect(image.set_duration(9.8)\
                        .set_start(i*9.8)\
                        .set_pos(("center", "center")))
                        #.resize(lambda t: 1+(t/9.8)/6)\
            
            background = CompositeVideoClip([background, image])
        
        background = CompositeVideoClip([
                        background,
                        ColorClip((video_maker.width, video_maker.height), (0,0,0))\
                            .set_opacity(0.8)\
                            .set_duration(59)
                        ])
        return [background]
    
    def make_content(self, video_maker):
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

    def make_watermark(self, video_maker):
      return []
    
    @staticmethod
    # Returns a random image, from Google Image, related to the query
    def get_related_image(query, temp_image_dir = './image_dir_temp/'):
        
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