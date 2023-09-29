from VideoMaker import *

def create_video(coordinator_class, content_factory_class, arguments):
    content_factory = content_factory_class(arguments)
    
    video_coordinator = coordinator_class(
        arguments['subject'],
        content_factory.get_content(arguments['subject'], coordinator_class.standardGPTPrompt),
        'Georgia-Bold',
        'Georgia')

    video_maker = VideoMaker(
        video_coordinator,
        ('h', arguments['height']) if arguments['height'] else ('w', arguments['width']),
        arguments['aspect_ratio'],
        arguments['fps'])

    video_maker.save((arguments['subject'] + '.mp4') if not arguments['output'] else arguments['output'])