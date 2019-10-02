from src.basics.basics import Position

import random
from collections import deque
from dataclasses import dataclass


class Generator(object):
    @dataclass
    class GeneratorState:
        height: int
        width: int
        map: list

    def __init__(self, settings=None):
        self._width = settings['width']
        self._height = settings['height']
        self._map_visited = [[False] * self._width for _ in range(self._height)]

    def create(self):
        self._create_map()

    def get_state(self):
        return self.GeneratorState(self._height, self._width, self._map_visited)

    def _create_map(self):
        start_position = Position(1, 1)
        self._map_visited = [[False] * self._width for _ in range(self._height)]
        self._map_visited[start_position.y][start_position.x] = True

        q = deque()
        q.append(start_position)

        while q.__len__():
            current_cell = q.popleft()

            neighbours = self._get_neighbours(current_cell)

            if neighbours.__len__():
                next_cell = random.choice(neighbours)
                q.appendleft(current_cell)
                q.appendleft(next_cell)

                self._map_visited[next_cell.y][next_cell.x] = True
                self._map_visited[(current_cell.y + next_cell.y) // 2][(current_cell.x + next_cell.x) // 2] = True

    def _get_neighbours(self, _current_cell, any=False):
        left = Position(_current_cell.x - 2, _current_cell.y)
        right = Position(_current_cell.x + 2, _current_cell.y)
        up = Position(_current_cell.x, _current_cell.y - 2)
        down = Position(_current_cell.x, _current_cell.y + 2)

        directions = [up, right, down, left]
        neighbours = []

        for direction in directions:
            if direction.x >= 0 and direction.x < self._width and direction.y >= 0 and direction.y < self._height:
                if not self._map_visited[direction.y][direction.x] or any:
                    neighbours.append(direction)

        return neighbours
