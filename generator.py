#/usr/bin/python3.7
from dataclasses import dataclass

import yaml
import random
import math
from collections import deque

from src.parser import Parser


@dataclass
class Position:
    x: int
    y: int


class Generator(object):
    DEFAULT_MAP_NAME = './maps/new_map.yaml'
    DEFAULT_TILE_SIZE = 0.585

    def __init__(self, settings=None):
        self._width = settings['width']
        self._height = settings['height']
        self._map = [['straight/W'] * self._width for _ in range(self._height)]
        self._data = {}
        self._objects = []

    def create(self):
        self._create_map()
        self._create_objects()

        self._data = {
            'tiles': self._map,
            'objects': self._objects,
            'tile_size': self.DEFAULT_TILE_SIZE
        }

    def _create_map(self):
        start_position = Position(1, 1)
        map_visited = [[False] * self._width for _ in range(self._height)]
        map_visited[start_position.y][start_position.x] = True

        q = deque()
        q.append(start_position)

        while q.__len__():
            current_cell = q.popleft()

            neighbours = self._get_neighbours(current_cell, map_visited)

            if neighbours.__len__():
                next_cell = random.choice(neighbours)
                q.appendleft(current_cell)
                q.appendleft(next_cell)

                map_visited[next_cell.y][next_cell.x] = True
                map_visited[(current_cell.y + next_cell.y) // 2][(current_cell.x + next_cell.x) // 2] = True

        for i in range(self._height):
            for j in range(self._width):
                self._map[i][j] = 'straight/W' if map_visited[i][j] else 'floor'

    def _get_neighbours(self, _current_cell, _map_visited, any=False):
        left = Position(_current_cell.x - 2, _current_cell.y)
        right = Position(_current_cell.x + 2, _current_cell.y)
        up = Position(_current_cell.x, _current_cell.y - 2)
        down = Position(_current_cell.x, _current_cell.y + 2)

        directions = [up, right, down, left]
        neighbours = []

        for direction in directions:
            if direction.x >= 0 and direction.x < self._width and direction.y >= 0 and direction.y < self._height:
                if not _map_visited[direction.y][direction.x] or any:
                    neighbours.append(direction)

        return neighbours

    def _create_objects(self):
        for _ in range(random.randint(150, 151)):
            duckie_pos = [1 + random.random(), 3 * random.random()]
            my_pos = [3.5, 1.5]
            vector = [duckie_pos[0] - my_pos[0], -duckie_pos[1] + my_pos[1]]

            self._objects.append({
                'height': 0.06,
                'kind': random.choice(['duckie', 'sign_blank']),
                'pos': duckie_pos, #[random.random() * self._width / 3, random.random() * self._height / 3],
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


if __name__ == '__main__':
    map_settings = Parser.parse()
    generator = Generator(map_settings)

    generator.create()
    generator.save()
