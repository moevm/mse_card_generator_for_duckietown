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
    DEBUG = False

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
        self.__cannot_be_used_as_node = []

        self._random = GeneratorRandom(self._width, self._height)
        self._state = self.GeneratorState(self._height, self._width, list())

    def create(self):
        self._create_map()
        self._generate_state()

    def get_state(self):
        return self._state

    def _on_board(self, p):
        return 0 <= p.x < self._width and 0 <= p.y < self._height

    def _accept(self, _cell):
        _cell.under_construction = False
        _cell.accepted = True

    def _create_map(self):
        accepted_roads = self._create_first_cycle()
        under_construction_roads = []
        checked_cells = []

        start = random.choice(accepted_roads)
        current_cell = start
        is_new_cycle = True
        num = 0

        while True:
            if self.DEBUG:
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

                #print(''.join(['\033[F'] * (self._height + 2)))

            if is_new_cycle:
                num += 1

                for cell in checked_cells:
                    cell.checked = False

                checked_cells.clear()
                begin, current_cell = self._first_cycle_cell(current_cell)

                if not begin:
                    return

                current_cell.under_construction = True
                under_construction_roads.append(begin)
                under_construction_roads.append(current_cell)
                is_new_cycle = False
                continue

            if num == 50:
                return

            neighbours = self._get_neighbours(current_cell, lambda c: not c.checked and not c.accepted and not c.under_construction and len(self._get_neighbours(c, lambda _: _.under_construction)['requested']) == 1)

            actual = []

            for next_cell in neighbours['requested']:
                neibs = self._get_neighbours(next_cell, lambda c: c.accepted)

                if len(neibs['requested']) == 1:
                    if neibs['requested'][0] in (self._get_neighbours(under_construction_roads[-2], lambda _: True)['all']):
                        continue

                    under_construction_roads.append(next_cell)
                    next_cell.under_construction = True

                    for cell in under_construction_roads:
                        self._accept(cell)

                    accepted_roads.extend(under_construction_roads[1:])
                    current_cell = random.choice(accepted_roads)
                    under_construction_roads = [current_cell]
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
                under_construction_roads.remove(current_cell)

                if len(under_construction_roads) == 1:
                    last = under_construction_roads[0]
                    last.under_construction = False
                    #self.__cannot_be_used_as_node.append(last)
                    is_new_cycle = True
                else:
                    current_cell = under_construction_roads[-1]

                continue

            nc = random.choice(actual)

            current_cell = nc
            under_construction_roads.append(nc)
            nc.under_construction = True

    def _generate_state(self):
        map = [[0] * self._width for _ in range(self._height)]

        for i in range(self._height):
            for j in range(self._width):
                cell = self._cells[i][j]

                if not cell.accepted:
                    map[i][j] = 0
                    continue

                neighbours = self._get_neighbours(cell, lambda c: c.accepted)['requested']
                neighbour_data = 0

                for neighbour in neighbours:
                    if neighbour.position.y < cell.position.y:
                        neighbour_data |= 1
                    elif neighbour.position.x > cell.position.x:
                        neighbour_data |= 2
                    elif neighbour.position.y > cell.position.y:
                        neighbour_data |= 4
                    elif neighbour.position.x < cell.position.x:
                        neighbour_data |= 8

                map[i][j] = neighbour_data

        self._state = self.GeneratorState(self._height, self._width, map)

    def _first_cycle_cell(self, _current_cell):
        while True:
            neibs = self._get_neighbours(_current_cell, lambda c: not c.under_construction and not c.accepted and len(self._get_neighbours(c, lambda _: _.accepted)['requested']) == 1)
            requested = neibs['requested']
            correct_cells = []

            if len(requested) == 0:
                self.__cannot_be_used_as_node.append(_current_cell)
                lst = list(filter(lambda c: c not in self.__cannot_be_used_as_node, neibs['roads']))

                if len(lst) == 0:
                    return [None, None]

                _current_cell = random.choice(lst)

                continue

            for _cell in requested:
                dx = _cell.position.x - _current_cell.position.x
                dy = _cell.position.y - _current_cell.position.y

                counter = 0
                flag = True

                current_position = Position(_cell.position.x, _cell.position.y)

                while self._on_board(current_position):
                    if self._cells[current_position.y][current_position.x].accepted and flag:
                        counter += 1
                        flag = False
                    else:
                        flag = True

                    current_position.x += dx
                    current_position.y += dy

                if counter % 2 == 0:
                    correct_cells.append(_cell)

            if len(correct_cells) == 0:
                self.__cannot_be_used_as_node.append(_current_cell)
                lst = list(filter(lambda c: c not in self.__cannot_be_used_as_node, neibs['roads']))

                if len(lst) == 0:
                    return [None, None]

                _current_cell = random.choice(lst)

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
