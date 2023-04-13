from VideoMaker import *

def create_video(coordinator_class, arguments, content_factory):
    video_coordinator = coordinator_class(
        arguments['subject'],
        content_factory.getContent(arguments['subject'], coordinator_class.standardGPTPrompt),
        'Merriweather-Bold',
        'Merriweather-Regular')

    video_maker = VideoMaker(
        video_coordinator,
        ('h', arguments['height']) if arguments['height'] else ('w', arguments['width']),
        arguments['aspect_ratio'],
        arguments['fps'])

    video_maker.save((arguments['subject'] + '.mp4') if not arguments['output'] else arguments['output'])