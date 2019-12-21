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

        print('aaaaaaaaa')

        for i in range(state.height):
            for j in range(state.width):
                self._map[i][j] = self.CELLS[state.map[i][j]]

                if self._map[i][j] == 'floor':
                    building_type = random.choice(['duckie',
                                                   'tree',
                                                   'house'])

                    if random.randint(0, 3) == 0:
                        if building_type == 'house':
                            self._objects.append({
                                'height': 0.22, 'kind':building_type, 'pos': [j + 0.2925, i + 0.2925], 'rotate': 0
                            })
                        elif building_type == 'tree':
                            for _ in range(random.randint(3, 7)):
                                self._objects.append({
                                    'height': 0.22,
                                    'kind': building_type,
                                    'pos': [j + random.random() * self.DEFAULT_TILE_SIZE, i + random.random() * self.DEFAULT_TILE_SIZE],
                                    'rotate': 0
                                })
                        elif building_type == 'duckie':
                            for _ in range(random.randint(1, 4)):
                                self._objects.append({
                                    'height': 0.04,
                                    'kind': building_type,
                                    'pos': [j + random.random() * self.DEFAULT_TILE_SIZE, i + random.random() * self.DEFAULT_TILE_SIZE],
                                    'rotate': 0
                                })


                if state.map[i][j] == 14:
                    self._objects.append({'height': 0.24,'kind': random.choice(['trafficlight']),'pos': [j + 0.25, i],'rotate': 45,'static': True})
                if state.map[i][j] == 7:
                    self._objects.append({'height': 0.24,'kind': random.choice(['trafficlight']),'pos': [j, i + 0.25],'rotate': 45,'static': True})
                if state.map[i][j] == 11:
                    self._objects.append({'height': 0.24,'kind': random.choice(['trafficlight']),'pos': [j + 0.25, i + 1],'rotate': 135,'static': True})
                if state.map[i][j] == 13:
                    self._objects.append({'height': 0.24,'kind': random.choice(['trafficlight']),'pos': [j + 1, i + 0.25],'rotate': 315,'static': True})
                if state.map[i][j] == 15:
                    self._objects.append({'height': 0.24,'kind': random.choice(['trafficlight']),'pos': [j + 0.25, i + 0.25],'rotate': 45,'static': True})


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
                'kind': random.choice(['sign_blank']),
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
