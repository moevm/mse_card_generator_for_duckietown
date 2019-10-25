from src.generator import Generator

import random
import math
import yaml


class DuckietownMap(object):
    DEFAULT_MAP_NAME = './maps/new_map.yaml'
    DEFAULT_TILE_SIZE = 0.585

    CELLS = {
        0: 'floor',
        5: 'straight/N',
        10: 'straight/E',
        3: 'curve_right/W',
        6: 'curve_right/N',
        12: 'curve_left/N',
        9: 'curve_left/E',
        7: '3way_left/S',
        11: '3way_left/E',
        14: '3way_left/W',
        13: '3way_left/N',
        15: '4way'
    }

    def __init__(self, generator=None):
        self._map = list()
        self._data = {}
        self._objects = []
        self._generator = generator

    def set_generator(self, generator):
        self._generator = generator

    def new(self):
        self._generator.create()
        state = self._generator.get_state()

        self._map = [['straight/W'] * state.width for _ in range(state.height)]

        for i in range(state.height):
            for j in range(state.width):
                print(state.map[i][j], j, i)
                self._map[i][j] = self.CELLS[state.map[i][j]]

        self._create_objects()

        self._data = {
            'tiles': self._map,
            'objects': self._objects,
            'tile_size': self.DEFAULT_TILE_SIZE
        }

        return self

    def _create_objects(self):
        for _ in range(random.randint(150, 151)):
            duckie_pos = [1 + random.random(), 3 * random.random()]
            my_pos = [3.5, 1.5]
            vector = [duckie_pos[0] - my_pos[0], -duckie_pos[1] + my_pos[1]]

            self._objects.append({
                'height': 0.06,
                'kind': random.choice(['duckie', 'sign_blank']),
                'pos': duckie_pos,
                'rotate': 160 + math.degrees(math.atan2(vector[1], vector[0])),
                'static': True
            })

        self._objects.append({
            'height': 0.06,
            'kind': random.choice(['bus']),
            'pos': [2.1, 1.5],
            'rotate': 90,
            'static': True
        })

    def save(self, file_name=DEFAULT_MAP_NAME):
        with open(file_name, 'w') as fout:
            fout.write(yaml.dump(self._data))
