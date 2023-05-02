import argparse, sys

def get_arguments():
    parser = argparse.ArgumentParser(
        description='Automatic video creation using GPT',
    )

    parser.add_argument('-s', '--subject',
                        help='Video subject',
                        required=True, type=str)
    
    parser.add_argument('-k', '--api-key',
                        help='OpenAI API key',
                        required=True, type=str)
    
    parser.add_argument('-c', '--coordinator',
                        help='Coordinator for the video. It is what defines the "model" of your video. Currently only SixFacts is available.',
                        required=True, type=str,
                        choices=['SixFacts'])
    
    size_group = parser.add_mutually_exclusive_group(required=True)

    size_group.add_argument('-j', '--height',
                            help='Video height',
                            type=int)
    
    size_group.add_argument('-w', '--width',
                            help='Video width',
                            type=int)
    
    parser.add_argument('-a', '--aspect-ratio',
                        help='Video aspect ratio',
                        type=float,
                        default=9/16)
    
    parser.add_argument('-f', '--fps',
                        help='Video FPS',
                        type=int,
                        default=25)
    
    parser.add_argument('-o', '--output',
                        help='Video save location',
                        type=str)
    

    return vars(parser.parse_args(sys.argv[1:]))