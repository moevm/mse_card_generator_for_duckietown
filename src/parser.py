import argparse


class Parser(object):
    def __init__(self):
        pass

    @staticmethod
    def parse():
        parser = argparse.ArgumentParser()
        parser.add_argument('--size', default='7x7', type=str, action='store', help='map size')

        width, height = list(map(int, (parser.parse_args().size).split('x')))

        return {
            'width': width,
            'height': height
        }
