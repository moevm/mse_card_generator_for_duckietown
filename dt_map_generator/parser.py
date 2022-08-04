import argparse
import random


class Parser(object):
    def __init__(self):
        pass

    @staticmethod
    def parse():
        parser = argparse.ArgumentParser()
        parser.add_argument('--size', default='7x7', type=str, action='store', help='map size')
        parser.add_argument('--crossroad_count', default='', type=str, action='store',
                            help='crossroads count and type\nFor example:\n4\n4T\n4Q\n4T2Q')
        parser.add_argument('--road_length', default=15, type=str, action='store', help='maximum road length')
        parser.add_argument('--cycles', default=-1, type=int, action='store', help='cycles count')
        parser.add_argument('--path', default='./maps', type=str, action='store', help='save map directory')

        width, height = list(map(int, (parser.parse_args().size).split('x')))
        length = int(parser.parse_args().road_length)
        triple, quad = Parser.parse_crossroads(parser.parse_args().crossroad_count)
        cycles = parser.parse_args().cycles
        path = parser.parse_args().path

        if cycles > 0:
            if cycles != 1 + quad + 0.5 * triple:
                raise Exception("params collision")

        return {
            'width': width,
            'height': height,
            'length': length,
            'path': path,
            'crossroads_data': {
                'triple': triple,
                'quad': quad
            }
        }

    @classmethod
    def parse_crossroads(cls, s: str):
        if s.isdigit():
            n = int(s)
            t = random.randint(0, n // 2) * 2
            q = n - t
            return t, q
        else:
            data = s.split('.')
            output = [0, 0]

            for c in data:
                it = 0 if c[-1] == 'T' else 1

                if c[:-1].isdigit():
                    output[it] = int(c[:-1])
                elif c[:-1] == 'x':
                    output[it] = random.randint(0, 3)

            return output
