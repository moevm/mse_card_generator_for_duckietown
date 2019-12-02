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
            self.can_be_used_as_node = False
            self.checked = False

    def __init__(self, settings=None):
        self._width = settings['width']
        self._height = settings['height']
        self._crossroads_data = settings['crossroads_data']
        self._current_road_length = 0
        self._max_length = settings['length']

        self._cells = [[self.Cell(Position(x, y)) for x in range(self._width)] for y in range(self._height)]
        self.__cannot_be_used_as_node = []

        self._random = GeneratorRandom(self._width, self._height)
        self._state = self.GeneratorState(self._height, self._width, list())

    def create(self):
        self._create()
        self._generate_state()

    def get_state(self):
        return self._state

    def _all_crossroads_created(self):
            return self._crossroads_data['triple'] == 0 and self._crossroads_data['quad'] == 0

    def correct_cycle_node_condition(self, _cell):
        return True

    def debug(self):
        if self.DEBUG:
            print()

            for i in range(self._height):
                for j in range(self._width):
                    if self._cells[i][j].accepted:
                        print('\033[92m' + '#' + '\x1b[0m', end=' ')
                    elif self._cells[i][j].under_construction:
                        print('\033[91m' + '#' + '\x1b[0m', end=' ')
                    else:
                        print('\033[90m' + '0' + '\x1b[0m', end=' ')

                print()

            # print(''.join(['\033[F'] * (self._height + 2)))

    def _on_board(self, p):
        return 0 <= p.x < self._width and 0 <= p.y < self._height

    def _accept(self, _cell):
        _cell.under_construction = False
        _cell.accepted = True

    def _create(self):
        accepted_cells = self._create_first_cycle()

        while not self._all_crossroads_created():
            if not self._add_layer(accepted_cells):
                print('aaaa')
                break

            self.debug()
            print(self._crossroads_data['triple'])

    def _crossroads_block(self, *_cells):
        for _cell in _cells:
            for neighbour in self._get_neighbours(_cell, lambda c: c.accepted)['requested']:
                neighbour.can_be_used_as_node = False

    def _get_correct_cycle_ways(self, accepted_cells, condition, cannot_be_used_as_node_list, ways_count):
        random.shuffle(accepted_cells)

        for cell in accepted_cells:
            if cell not in cannot_be_used_as_node_list and condition(cell):
                neighbours = self._get_neighbours(cell, lambda c: not c.accepted)['requested']
                ways = []

                for neighbour in neighbours:
                    if len(self._get_neighbours(neighbour, lambda c: c.accepted)['requested']) == 1:
                        ways.append(neighbour)

                if len(ways) >= ways_count:
                    return cell, ways

        return None, None

    def _validate_path(self, _path, _node):
        if _path:
            begin = _node
            end = self._get_neighbours(_path[-1], lambda c: c.accepted)['requested'][0]

            for cell in _path:
                self._accept(cell)
                cell.can_be_used_as_node = True

            self._crossroads_block(begin, end)

            return True

        return False

    def _add_layer(self, accepted_cells):
        node = None
        cannot_be_used_as_node = []

        def node_neighbours_assert(_node: Generator.Cell, _cell: Generator.Cell) -> bool:
            neighbours = self._get_neighbours(_cell, lambda c: c.accepted)['requested']

            for neighbour in neighbours:
                nbs = self._get_neighbours(neighbour, lambda c: c.accepted)['requested']

                if _node in nbs:
                    return False

                for nb in nbs:
                    if len(self._get_neighbours(nb, lambda c: c.accepted)['requested']) >= 3:
                        return False

            return True

        transition_condition = lambda c: not c.accepted and \
                                         not c.under_construction and \
                                         len(self._get_neighbours(c, lambda _c: _c.under_construction)[
                                                 'requested']) <= 1 and \
                                         node_neighbours_assert(node, c)
        algorithm_end_condition = lambda c: len(self._get_neighbours(c, lambda _c: _c.accepted)['requested']) == 1 and \
                                            len(self._get_neighbours(c, lambda _c: _c.under_construction)[
                                                    'requested']) == 1

        while True:
            if self._crossroads_data['quad'] > 0:
                node, ways = self._get_correct_cycle_ways(accepted_cells, self.correct_cycle_node_condition,
                                                          cannot_be_used_as_node, ways_count=2)

                if not node:
                    return False

                for current_cell in ways:
                    aec = None
                    tc = None

                    if self._crossroads_data['triple'] == 0 or True:
                        aec = lambda c: algorithm_end_condition(c) and \
                                        node in self._get_neighbours(c, lambda _c: _c.accepted)['requested']
                        tc = lambda c: transition_condition(c) and \
                                       (len(self._get_neighbours(c, lambda _c: _c.accepted)['requested']) == 0 or
                                        (len(self._get_neighbours(c, lambda _c: _c.accepted)['requested']) == 1) and
                                        node in self._get_neighbours(c, lambda _c: _c.accepted)['requested'] and
                                        self._current_road_length != 2)

                    path = self._path_finder(current_cell, end=None, transition_condition=tc,
                                             algorithm_end_condition=aec)

                    if not self._validate_path(path, node):
                        cannot_be_used_as_node.append(node)
                        break

                    accepted_cells.extend(path)
                    self._crossroads_data['quad'] -= 1

                    return True
            elif self._crossroads_data['triple'] > 0:
                node, ways = self._get_correct_cycle_ways(accepted_cells, self.correct_cycle_node_condition,
                                                          cannot_be_used_as_node, ways_count=1)

                print('node = {}'.format(node))

                if not node:
                    return False

                for current_cell in ways:
                    aec = None
                    tc = None

                    aec = lambda c: algorithm_end_condition(c) and \
                                    node not in self._get_neighbours(c, lambda _c: _c.accepted)['requested']
                    tc = tc = lambda c: transition_condition(c)

                    path = self._path_finder(current_cell, end=None, transition_condition=tc,
                                             algorithm_end_condition=aec)

                    if not self._validate_path(path, node):
                        cannot_be_used_as_node.append(node)
                        continue

                    accepted_cells.extend(path)
                    self._crossroads_data['triple'] -= 2

                    return True

                continue
            break

    def _path_finder(self, begin, end=None, transition_condition=lambda c: True,
                     algorithm_end_condition=lambda c: True):
        if end:
            algorithm_end_condition = lambda c: c == end

        print(begin)

        queue = deque()
        queue.append(begin)
        current_cell = begin
        current_cell.under_construction = True
        current_cell.checked = True
        checked_neighbours = {
            current_cell: []
        }

        self._current_road_length = 1

        while not algorithm_end_condition(current_cell) and queue.__len__() > 0:
            #self.debug()

            neighbours = self._get_neighbours(current_cell, lambda c: transition_condition(c) and \
                                                                      self._current_road_length != self._max_length and \
                                                                      c not in checked_neighbours[current_cell])

            if len(neighbours['requested']) == 0:
                current_cell.under_construction = False
                self._current_road_length -= 1
                queue.remove(current_cell)
            else:
                requested = neighbours['requested']
                flag = False

                for cell in requested:
                    if algorithm_end_condition(cell):
                        current_cell = cell
                        flag = True

                        break

                if not flag:
                    next_cell = random.choice(requested)
                    checked_neighbours[current_cell].append(next_cell)
                    checked_neighbours.update({
                        next_cell: []
                    })

                    current_cell = next_cell
                    current_cell.under_construction = True

                queue.append(current_cell)
                self._current_road_length += 1

            if queue.__len__() > 0:
                current_cell = queue[-1]

        self._current_road_length = 0

        return list(queue)

    def _find_correct_cycle_node(self, _accepted_cells, _condition):
        random.shuffle(_accepted_cells)

        for _cell in _accepted_cells:
            if _cell.can_be_used_as_node and _condition(_cell):
                return _cell

    def _find_node_possible_way(self, _node):
        node_neighbours = self._get_neighbours(_node, lambda c: not c.accepted)
        requested = node_neighbours['requested']

        if len(requested) > 0:
            possible_ways = []

            for _cell in node_neighbours['requested']:
                if len(self._get_neighbours(_cell, lambda _c: _c.accepted)['requested']) != 1:
                    continue

                possible_ways.append(_cell)

            return possible_ways

        return None

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

    def _create_first_cycle(self, max_length=10):
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
            cell.can_be_used_as_node = True

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

    @property
    def cells(self):
        return self._cells
