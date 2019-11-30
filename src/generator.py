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
<<<<<<< HEAD
    DEBUG = False
=======
    DEBUG = True
>>>>>>> 4aa3dc94cbf54dd1170de3e4e3a0390d2aad63fd

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
<<<<<<< HEAD
            self.checked = False
            self.num = -1
=======
            self.can_be_used_as_node = False
            self.checked = False
>>>>>>> 4aa3dc94cbf54dd1170de3e4e3a0390d2aad63fd

    def __init__(self, settings=None):
        self._width = settings['width']
        self._height = settings['height']
<<<<<<< HEAD
=======
        self._crossroads_data = settings['crossroads_data']
        self._current_road_length = 0
        self._max_length = 12

>>>>>>> 4aa3dc94cbf54dd1170de3e4e3a0390d2aad63fd
        self._cells = [[self.Cell(Position(x, y)) for x in range(self._width)] for y in range(self._height)]
        self.__cannot_be_used_as_node = []

        self._random = GeneratorRandom(self._width, self._height)
        self._state = self.GeneratorState(self._height, self._width, list())

    def create(self):
<<<<<<< HEAD
        self._create_map()
=======
        self._create()
>>>>>>> 4aa3dc94cbf54dd1170de3e4e3a0390d2aad63fd
        self._generate_state()

    def get_state(self):
        return self._state

<<<<<<< HEAD
=======
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

>>>>>>> 4aa3dc94cbf54dd1170de3e4e3a0390d2aad63fd
    def _on_board(self, p):
        return 0 <= p.x < self._width and 0 <= p.y < self._height

    def _accept(self, _cell):
        _cell.under_construction = False
        _cell.accepted = True

<<<<<<< HEAD
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
=======
    def _create(self):
        accepted_cells = self._create_first_cycle()

        while not self._all_crossroads_created():
            if not self._add_layer(accepted_cells):
                break

            self.debug()

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
>>>>>>> 4aa3dc94cbf54dd1170de3e4e3a0390d2aad63fd

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

<<<<<<< HEAD
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
=======
    def _create_first_cycle(self, max_length=10):
>>>>>>> 4aa3dc94cbf54dd1170de3e4e3a0390d2aad63fd
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
<<<<<<< HEAD
=======
            cell.can_be_used_as_node = True
>>>>>>> 4aa3dc94cbf54dd1170de3e4e3a0390d2aad63fd

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
