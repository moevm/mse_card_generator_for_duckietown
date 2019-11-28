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
    DEBUG = True

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
            self.scanned = False
            self.num = -1

    def __init__(self, settings=None):
        self._width = settings['width']
        self._height = settings['height']
        self._cells = [[self.Cell(Position(x, y)) for x in range(self._width)] for y in range(self._height)]
        self.__cannot_be_used_as_node = []

        self._random = GeneratorRandom(self._width, self._height)
        self._state = self.GeneratorState(self._height, self._width, list())

    def create(self):
        self._create()
        self._generate_state()

    def get_state(self):
        return self._state

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

    def _scanning(self, _node, condition):
        cross_cell, another_cross_cell = self._get_neighbours(_node, condition)['requested']
        current_cell = cross_cell
        current_cell.scanned = True
        edge_cells = [current_cell]
        correct_flag = True

        while True:
            nbs = self._get_neighbours(current_cell, lambda c: c.accepted and not c.scanned)['requested']

            if len(nbs) > 0:
                current_cell = nbs[0]
                current_cell.scanned = True
                edge_cells.append(current_cell)
            else:
                break

        current_cell = self._get_neighbours(cross_cell, lambda c: not c.accepted)['requested'][0]
        dx = current_cell.position.x - cross_cell.position.x
        dy = current_cell.position.y - cross_cell.position.y
        flag = True

        print('start position = {}'.format(current_cell.position))
        print('dx = {}\ndy = {}'.format(dx, dy))

        while self._on_board(current_cell.position):
            cell = self._cells[current_cell.position.y][current_cell.position.x]

            if (cell.scanned or cell.checked) and not flag:
                flag = True
            elif (not cell.scanned or not cell.checked) and cell.accepted:
                flag = False

            current_cell.position.x += dx
            current_cell.position.y += dy

        print('state = {}'.format(flag))

        if not flag:
            return [True, edge_cells]
        else:
            for cell in edge_cells:
                cell.scanned = False

            return [False, [another_cross_cell]]

    def _create(self):
        accepted_cells = self._create_first_cycle()

        for i in range(10):
            cells_for_remove = self._prunning(self._add_layer(accepted_cells))

            for cell in cells_for_remove:
                cell.accepted = False
                cell.scanned = False

            self.debug()

    def _prunning(self, new_layer):
        begin = new_layer[0]
        end = new_layer[-1]

        begin.scanned = True
        end.scanned = True
        checked_cells = [begin, end]
        output = []

        node = begin

        result = self._scanning(node, lambda c: c.accepted and c not in [new_layer[1], new_layer[-2]])

        if result[0]:
            begin.scanned = False
            end.scanned = False

            return result[1]
        else:
            walker = result[1][0]
            output.append(walker)

            while True:
                nbs = self._get_neighbours(walker, lambda c: c.accepted and not c.scanned)['requested']

                if len(nbs) > 0:
                    walker = nbs[0]
                    walker.scanned = True
                    output.append(walker)
                else:
                    begin.scanned = False
                    end.scanned = False

                    return output

    def _add_layer(self, accepted_cells):
        while True:
            node = self._find_correct_cycle_node(accepted_cells)

            if not node:
                return True

            ways = self._find_node_possible_way(node, lambda c: not c.accepted)

            if not ways:
                node.can_be_used_as_node = False
                continue

            for current_cell in ways:
                path = self._backtracking_path_finder(node, current_cell)

                if path:
                    accepted_cells.extend(path[1:-1])
                    return path
                elif current_cell == ways[-1]:
                    node.can_be_used_as_node = False

    def _backtracking_path_finder(self, node, begin, end=None, conditions=[lambda: True]):
        current_cell = begin
        under_construction_cells = [node, begin]
        checked_cells = []

        node.under_construction = True
        current_cell.under_construction = True

        while True:
            self.debug()

            neighbours = self._get_neighbours(current_cell, lambda c: not c.checked and not c.accepted and not c.under_construction and len(self._get_neighbours(c, lambda _: _.under_construction)['requested']) == 1)
            actual_cells = []

            for neighbour in neighbours['requested']:
                nbs = self._get_neighbours(neighbour, lambda c: c.accepted)
                nbs_req = nbs['requested']

                print(len(nbs_req))

                if len(nbs_req) == 1:
                    if nbs_req[0] in self._get_neighbours(under_construction_cells[-2], lambda c: True)['requested'] or nbs_req[0] in self._get_neighbours(node, lambda c: True)['requested']:
                        continue

                    neighbour.under_construction = True
                    under_construction_cells.append(neighbour)
                    under_construction_cells.append(nbs_req[0])

                    for cell in under_construction_cells:
                        self._accept(cell)
                        cell.can_be_used_as_node = True

                    for cell in checked_cells:
                        cell.checked = False

                    return under_construction_cells
                elif len(nbs_req) == 0:
                    if len(list(filter(lambda c: c.under_construction, nbs['all']))) != 1:
                        continue

                    actual_cells.append(neighbour)

            if len(actual_cells) == 0:
                current_cell.checked = True
                checked_cells.append(current_cell)
                current_cell.under_construction = False
                under_construction_cells.pop()

                if len(under_construction_cells) == 1:
                    last = under_construction_cells[-1]
                    last.under_construction = False
                    last.can_be_used_as_node = True

                    for cell in checked_cells:
                        cell.checked = False

                    return None
                else:
                    current_cell = under_construction_cells[-1]
            else:
                current_cell = random.choice(actual_cells)
                current_cell.under_construction = True
                under_construction_cells.append(current_cell)

    def _find_correct_cycle_node(self, _accepted_cells):
        random.shuffle(_accepted_cells)

        for _cell in _accepted_cells:
            if _cell.can_be_used_as_node:
                return _cell

    def _find_node_possible_way(self, _node, condition, prunning=False):
        node_neighbours = self._get_neighbours(_node, condition)
        requested = node_neighbours['requested']

        print('len = {}'.format(len(requested)))
        print('node position = {}'.format(_node.position))

        if len(requested) == 2:
            if (requested[0].position.x == requested[1].position.x or requested[0].position.y == requested[1].position.y) and not prunning:
                return None

            possible_ways = []

            for _cell in node_neighbours['requested']:
                print(_cell.position)

                dx = _cell.position.x - _node.position.x
                dy = _cell.position.y - _node.position.y
                wall_road_flag = False
                current_position = Position(_node.position.x, _node.position.y)
                count = 0

                if len(self._get_neighbours(_cell, lambda _c: _c.accepted)['requested']) != 1 and not prunning:
                    continue

                while self._on_board(current_position):
                    if self._cells[current_position.y][current_position.x].accepted and wall_road_flag:
                        count += 1
                        wall_road_flag = False
                    elif not self._cells[current_position.y][current_position.x].accepted:
                        wall_road_flag = True

                    current_position.x += dx
                    current_position.y += dy

                if count % 2 == 0:
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
