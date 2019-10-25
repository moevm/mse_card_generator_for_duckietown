#/usr/bin/python3.7

from src.parser import Parser
from src.generator import Generator
from src.duckietown_map import DuckietownMap


if __name__ == '__main__':
    DuckietownMap(Generator(Parser.parse())).new().save()
