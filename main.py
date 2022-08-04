from dt_map_generator.parser import Parser
from dt_map_generator.generator import Generator
from dt_map_generator.duckietown_map import DuckietownMap


if __name__ == '__main__':
    DuckietownMap(Generator(Parser.parse())).new().save()
