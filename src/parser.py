import argparse
import random

class Parser(object):
    def __init__(self):
        pass

    @staticmethod
    def parse():
        parser = argparse.ArgumentParser()
        parser.add_argument('--size', default='7x7', type=str, action='store', help='map size')
        parser.add_argument('--crossroad_count', default='3', type=str, action='store', help='crossroads count and type\nFor example:\n4\n4T\n4Q\n4T2Q')

        width, height = list(map(int, (parser.parse_args().size).split('x')))
        crossroads_count = int(parser.parse_args().crossroad_count)
        triple = random.randint(0, crossroads_count - 1)
        quad = crossroads_count - triple

        return {
            'width': width,
            'height': height,
            'max_road_length': 0.1 * width * height,
            'crossroads_data': {
                'triple': triple,
                'quad': quad
            }
        }
