"""
Запуск: pytest из директории tests (mse_card_generator_for_duckietown/tests/)
Больше информации: pytest -v

"""

"""
Данный скрипт тестирует функции "_get_neighbours", "_generate_state" класса "Generator" из файла src/generator.py
"""

import sys

sys.path.append('..')

import pytest
from json import load

from src.generator import Generator
from src.basics.basics import Position

with open('test_suit.json', 'r', encoding='utf-8') as f:
    data = load(f)

generator = Generator({
    'width':5,
    'height':5,
    'length': 10,
    'crossroads_data': {
        'triple': 1,
        'quad': 1
    }
})

generator_large = Generator({
    'width':9,
    'height':9,
    'length': 10,
    'crossroads_data': {
        'triple': 1,
        'quad': 1
    }
})


@pytest.mark.parametrize('param', data['params'])
def test_get_neighbours_0(param):
    inp1, inp2, answer = param

    cells = [generator._cells[3][3], generator._cells[2][2], generator._cells[1][3]]

    for cell in cells:
        cell.accepted = True

    neighbours = generator._get_neighbours(Generator.Cell(Position(inp1, inp2)), lambda c: c.accepted)
    generator.debug()

    assert len(neighbours['roads']) == answer


@pytest.mark.parametrize('param', data['maps'])
def test__generate_state_1(param):
    inp1, answer = param

    for i in range(5):
        for j in range(5):
            generator._cells[i][j].accepted = True if inp1[i][j] else False

    generate_state = generator._generate_state()
    generator.debug()

    print(answer)
    print(generator.get_state().map)

    assert generator.get_state().map == answer


@pytest.mark.parametrize('param', data['maps_large'])
def test__generate_state_2(param):
    inp1, answer = param

    for i in range(9):
        for j in range(9):
            generator_large._cells[i][j].accepted = True if inp1[i][j] else False

    generate_state = generator_large._generate_state()
    generator_large.debug()

    print(answer)
    print(generator_large.get_state().map)

    assert generator_large.get_state().map == answer
