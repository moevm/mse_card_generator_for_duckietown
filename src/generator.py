from src.basics.basics import Position

import random
import time
from collections import deque
from dataclasses import dataclass


class GeneratorRandom(object):
    def __init__(self, width, height):
        self._width = width
        self._height = height

    def position(self):
        return Position(random.randint(0, self._width - 1), random.randint(0, self._height - 1))


class Generator(object):
    ANY = lambda _: True

    @dataclass
    class GeneratorState:
        height: int
        width: int
        map: list

    class Cell(object):
        def __init__(self, position):
            self.position = position
            self.accepted = False
            self.under_construction = False
            self.checked = False
            self.num = -1

    def __init__(self, settings=None):
        self._width = settings['width']
        self._height = settings['height']
        self._cells = [[self.Cell(Position(x, y)) for x in range(self._width)] for y in range(self._height)]

        self._random = GeneratorRandom(self._width, self._height)

    def create(self):
        self._create_map()

    def get_state(self):
        return self.GeneratorState(self._height, self._width, [[self._cells[i][j].accepted for j in range(self._width)] for i in range(self._height)])

    def _on_board(self, p):
        return 0 <= p.x < self._width and 0 <= p.y < self._height

    def _set_acception(self, _cell):
        _cell.accepted = True

    def _create_map(self):
        __local_cells_buffer = self._create_first_cycle()
        __local_under_construction_cells_buffer = []
        checked_cells = []
        start = random.choice(__local_cells_buffer)
        current_cell = start
        is_new_cycle = True
        exception = None
        begin = None
        end = None
        num = 0

        while True:
            print()

            for i in range(self._height):
                for j in range(self._width):
                    if self._cells[i][j].accepted:
                        print('\033[92m' + '#' + '\x1b[0m', end=' ')
                    elif self._cells[i][j].under_construction:
                        print ('\033[91m' + '#' + '\x1b[0m', end=' ')
                    else:
                        print('\033[90m' + '0' + '\x1b[0m', end=' ')

                print()

            print(''.join(['\033[F'] * (self._height + 2)))

            if is_new_cycle:
                num += 1

                for cell in checked_cells:
                    cell.checked = False

                checked_cells.clear()
                begin, current_cell = self._first_cycle_cell(current_cell)

                if not begin:
                    return

                current_cell.under_construction = True
                __local_under_construction_cells_buffer.append(begin)
                __local_under_construction_cells_buffer.append(current_cell)
                is_new_cycle = False
                continue

            if num == 50:
                return

            neighbours = self._get_neighbours(current_cell, lambda c: not c.checked and not c.accepted and not c.under_construction and len(self._get_neighbours(c, lambda _: _.under_construction)['requested']) == 1)

            actual = []

            for next_cell in neighbours['requested']:

                neibs = self._get_neighbours(next_cell, lambda c: c.accepted)

                if len(neibs['requested']) == 1:
                    end = next_cell
                    #print('yey')

                    if neibs['requested'][0] in (self._get_neighbours(__local_under_construction_cells_buffer[-2], lambda _: True)['all']):
                        #print("aaaaaa")
                        continue

                    __local_under_construction_cells_buffer.append(next_cell)
                    next_cell.under_construction = True

                    for cell in __local_under_construction_cells_buffer:
                        cell.under_construction = False
                        cell.accepted = True

                    __local_cells_buffer.extend(__local_under_construction_cells_buffer[1:])
                    current_cell = random.choice(__local_cells_buffer)
                    __local_under_construction_cells_buffer = [current_cell]
                    is_new_cycle = True

                    break
                elif len(neibs['requested']) == 0:
                    if len(list(filter(lambda c: c.under_construction, neibs['all']))) != 1:
                        continue

                    actual.append(next_cell)
                else:
                    continue

            if is_new_cycle:
                continue

            if len(actual) == 0:
                current_cell.under_construction = False
                current_cell.checked = True
                checked_cells.append(current_cell)
                __local_under_construction_cells_buffer.remove(current_cell)

                if len(__local_under_construction_cells_buffer) == 1:
                    last = __local_under_construction_cells_buffer[0]
                    last.under_construction = False
                    is_new_cycle = True
                else:
                    current_cell = __local_under_construction_cells_buffer[-1]

                continue

            nc = random.choice(actual)

            current_cell = nc
            __local_under_construction_cells_buffer.append(nc)
            nc.under_construction = True

    def _first_cycle_cell(self, _current_cell):
        current_cycle_roads = []

        while True:
            neibs = self._get_neighbours(_current_cell, lambda c: not c.under_construction and not c.accepted and len(self._get_neighbours(c, lambda _: _.accepted)['requested']) == 1)
            requested = neibs['requested']
            correct_cells = []

            if len(requested) == 0:
                current_cycle_roads.append(_current_cell)
                lst = list(filter(lambda c: c not in current_cycle_roads, neibs['roads']))

                if len(lst) == 0:
                    return None

                _current_cell = random.choice(lst)

                continue

            #print(len(neibs['requested']))

            for _cell in requested:
                dx = _cell.position.x - _current_cell.position.x
                dy = _cell.position.y - _current_cell.position.y
                sum = 0
                flag = True

                #print(dx, dy)

                current_position = Position(_cell.position.x, _cell.position.y)

                while self._on_board(current_position):
                    if self._cells[current_position.y][current_position.x].accepted and flag:
                        sum += 1
                        flag = False
                    else:
                        flag = True

                    current_position.x += dx
                    current_position.y += dy

                if sum % 2 == 0:
                    correct_cells.append(_cell)

            #print(len(correct_cells))

            if len(correct_cells) == 0:
                current_cycle_roads.append(_current_cell)
                _current_cell = random.choice(list(filter(lambda c: c not in current_cycle_roads, neibs['roads'])))

                continue

            cell_node = random.choice(correct_cells)

            return _current_cell, cell_node

    def _create_first_cycle(self):
        center = Position(self._width // 2, self._height // 2)

        cells = [
            self._cells[center.y - 1][center.x - 1],
            self._cells[center.y - 1][center.x],
            self._cells[center.y - 1][center.x + 1],
            self._cells[center.y][center.x - 1],
            self._cells[center.y][center.x + 1],
            self._cells[center.y + 1][center.x - 1],
            self._cells[center.y + 1][center.x],
            self._cells[center.y + 1][center.x + 1]
        ]

        for cell in cells:
            cell.accepted = True

        return cells

    def _get_neighbours(self, _current_cell, request):
        position = _current_cell.position

        left = Position(position.x - 1, position.y)
        right = Position(position.x + 1, position.y)
        up = Position(position.x, position.y - 1)
        down = Position(position.x, position.y + 1)

        directions = [up, right, down, left]

        _cells = {
            'all': [],
            'requested': [],
            'roads': []
        }

        for direction in directions:
            if self._on_board(direction):
                _cell = self._cells[direction.y][direction.x]
                _cells['all'].append(_cell)

                if request(_cell):
                    _cells['requested'].append(_cell)

                if _cell.accepted or _cell.under_construction:
                    _cells['roads'].append(_cell)

        return _cells
